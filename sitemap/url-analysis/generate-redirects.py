# %%
# Read data from aggregated nginx access log file
from pathlib import Path
import re
from urllib.parse import unquote, urlparse
from collections import defaultdict
import pandas as pd

from constants import *

def diff_df(df1, df2):
    """
    Compares two dataframes and returns a dataframe with rows that are different or added.

    :param df1: First dataframe (e.g., df_canonicalized)
    :param df2: Second dataframe (e.g., df_redirects)
    :return: Dataframe containing differences and new rows
    """
    # Merge the dataframes
    merged_df = pd.merge(df1, df2, how='outer', indicator=True)

    # Filter to find rows that are different or only in df2
    df_differences = merged_df[merged_df['_merge'] != 'both']

    # Drop the '_merge' column
    df_differences.drop('_merge', axis=1, inplace=True)

    return df_differences

# Path to nginx acccess log file as the source of request URIs
nginx_access_log = INPUT_DIR / f'{ORIGINAL_DOMAIN}_access.csv'

# Load the data from CSV
df = pd.read_csv(nginx_access_log)
# Convert LAST_ACCESS to a datetime object
df[LAST_ACCESS] = pd.to_datetime(df[LAST_ACCESS], format='%d/%b/%Y:%H:%M:%S %z', utc=True)

# %%
# Consider only URLs that look valid

# Ignore URLs that contain malicious code
malicous_regex = (r"^/(?:admin|backup|blog|cms|console|data|debug|mailman|api|_?error)"
            + r"|\.(?:js|exe)\b" + r"|['\"+&]|\\x22|select*|/RK=0|/RS=\^"
            + r"|non-existing|\.well-known|81gzm|/wp-|2000/00/99|/basic-tex|2wCEAAgGBgcGB|autodiscover/|clientaccesspolicy|DbXmlInfo|phpunit|vWfM6kbCUIv|fa3c615d773|iVBORw0KGgo")
malicious_mask = df[REQUEST_URI].str.contains(malicous_regex, na=False, case=False, regex=True)

# Ignore URLs that contain URL-encoded characters such as %20|%23|%C3%(?:83|AE|AF|A2|82|html)|%E6%88|%22%20class=%22|...
encoded_mask_to_ignore = df[REQUEST_URI].str.contains(r'%[0-9A-F]{2}', na=False, case=False, regex=True)
# ...but keep URLs that contain `Page%28[^%]+%29` as those occur in URLs of the form `Page(/articles/_index.md)`
encoded_mask_to_keep = df[REQUEST_URI].str.contains(r'Page%28[^%]+index\.md%29', na=False, case=False, regex=True)
encoded_mask = encoded_mask_to_ignore & ~encoded_mask_to_keep

# Ignore URLs that contain 'http:' or 'https:'...
http_mask_to_ignore = df[REQUEST_URI].str.contains(r'https?:', na=False, case=False, regex=True)
# ...but keep URLs that contain ORIGINAL_DOMAIN
# Note: Since no static file hosting service will let URLs with scheme and host reach their
# URI processing engine, we can just ignore all URIs that begin with a scheme
# http_heimlicher_mask_to_keep = df[REQUEST_URI].str.contains(r'https?://' + ORIGINAL_HOST_MATCH_RE, na=False, case=False, regex=True)
#http_mask = http_mask_to_ignore & ~http_heimlicher_mask_to_keep
http_mask = http_mask_to_ignore

# Ignore URLs that contain '.php'...
php_mask_to_ignore = df[REQUEST_URI].str.contains('.php', na=False, case=False, regex=False)
# ... unless they contain 'doku.php'
doku_php_mask_to_keep = df[REQUEST_URI].str.contains('/doku.php', na=False, case=False, regex=False)
php_mask = php_mask_to_ignore & ~doku_php_mask_to_keep

# Ignore URLs that contain a file extension...
file_extension_mask_to_ignore = df[REQUEST_URI].str.contains(r'.', na=False, case=False, regex=False)
# ...unless they ontain '.pdf' or '.md'
file_extension_mask_to_keep = df[REQUEST_URI].str.contains(r'\.(?:xml|html|pdf|md)', na=False, case=False, regex=True)
file_extension_mask = file_extension_mask_to_ignore & ~file_extension_mask_to_keep

ignore_mask = malicious_mask | encoded_mask | http_mask | php_mask | file_extension_mask

# Split the DataFrame into two parts: valid and invalid URLs
# df_invalid_raw = df[ignore_mask]
df_keep = df[~ignore_mask]

# %%
# Clean up the valid URLs and remove the query string
# Add a column that contains the URL without query
def sanitize_url(url):
    # Replace multiple slashes with a single slash
    url = re.sub(r'(?<!:)//+', '/', url)
    return url

def url_without_query(url):
    # First, sanitize the URL
    sanitized_url = sanitize_url(url)

    # Parse the sanitized URL
    parsed_url = urlparse(sanitized_url)

    # Check if the URL is a complete URL (includes a scheme like http)
    if parsed_url.scheme and parsed_url.netloc:
        return parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    elif parsed_url.path.startswith('/'):
        # If it's just a path starting with '/', return the path
        return parsed_url.path
    else:
        # Invalid URL
        return None

# Apply the function to create a new column
df_cleaned_raw = df_keep.copy()
df_cleaned_raw[REQUEST_URI_WITHOUT_QUERY] = df_cleaned_raw[REQUEST_URI].apply(url_without_query)

# Create a mask to keep only non-None entries in REQUEST_URI_WITHOUT_QUERY
valid_url_mask = df_cleaned_raw[REQUEST_URI_WITHOUT_QUERY].notnull()

# Apply the mask to filter the DataFrame
df_cleaned = df_cleaned_raw[valid_url_mask]

# Replace column REQUEST_URI by REQUEST_URI_WITHOUT_QUERY
# Drop the original REQUEST_URI column
df_cleaned = df_cleaned.drop(columns=[REQUEST_URI])

# Rename REQUEST_URI_WITHOUT_QUERY to REQUEST_URI
df_cleaned = df_cleaned.rename(columns={REQUEST_URI_WITHOUT_QUERY: REQUEST_URI})

# Reorder the columns
df_cleaned = df_cleaned[COLUMNS_INPUT]
# %%
# Aggregate the cleaned URLs

# Sort by REQUEST_URI and then by LAST_ACCESS in descending order
df_aggregated = df_cleaned.sort_values(by=[REQUEST_URI, LAST_ACCESS], ascending=[True, False])

# Group by REQUEST_URI: add up the ACCESS_COUNT and keep only the LAST_ACCESS and the STATUS_CODE of the last access to the URL
df_aggregated = df_aggregated.groupby(REQUEST_URI).agg({
    ACCESS_COUNT: 'sum',  # Sum the ACCESS_COUNT
    LAST_ACCESS: 'first', # The first LAST_ACCESS in each group is the latest
    STATUS_CODE: 'first'  # Get the STATUS_CODE corresponding to the latest access
}).reset_index()

# Sort by ACCESS_COUNT from most frequent down and then by LAST_ACCESS from most recent down
df_aggregated = df_aggregated.sort_values(by=[ACCESS_COUNT, LAST_ACCESS], ascending=[False, False])
df_aggregated.to_csv(OUTPUT_DIR / 'access_log_urls.csv', index=False)
# %%
# Add a column that contains a canonicalized form of the URL
canonicalization_rules = [
    # (r'^https?://' + ORIGINAL_HOST_MATCH_RE + r'(?::[0-9]+)?(/(?:[^/" ]+/)*[^/" ]*)', r'^https?://' + ORIGINAL_HOST_MATCH_RE + r'(?::[0-9]+)?(/(?:[^/" ]+/)*[^/" ]*)$', r'\1'),
    (r'^/Page(?:[(]|%28)(.*)(?:(/[^./]*)|(?:/_?index\.md))(?:[)]|%29)$', None, r'\1\2/'),
    (r'^(/articles/)(?:[0-9]{4}/[0-9]{2}/[0-9]{2}/)([^/]+).*$', None, r'\1\2/'),
    (r'(.*?/)(?:atom|index|start|null).*', None, r'\1'),
    (r'(.*?/)page/[1-9].*', None, r'\1'),
    (r'^/(?:hints|(?:de/)?(?:categories|series|tags))', r'_', r'-'),
    (r'(.*?)(?:/index)?\.html.*', None, r'\1/'),
    (r'(^.*/[^./]+)$', None, r'\1/'),
]

def canonicalize_url(row):
    canonical_url = row[REQUEST_URI]
    # Apply all canonicalization rules in sequence
    for pattern, search_pattern, replacement in canonicalization_rules:
        if re.match(pattern, canonical_url):
            canonical_url = re.sub(search_pattern if search_pattern else pattern,
                                   replacement, canonical_url)
    if canonical_url != row[REQUEST_URI]:
        pass
    return canonical_url

# Apply the function and create 'df_canonicalized'
df_canonicalized = df_aggregated.copy()
df_canonicalized[REQUEST_URI_CANONICAL] = df_aggregated.apply(canonicalize_url, axis=1)
df_canonicalized = df_canonicalized.reset_index()
df_canonicalized = df_canonicalized[COLUMNS_INPUT_CANONICAL]

def test_substitution(df, test_set, substituted_column=REDIRECT_URI):
    for idx, test in enumerate(test_set):
        uri_test, uri_result = test
        uri_regex = r'^' + uri_test + r'$'
        redirect_match = df[df[REQUEST_URI].str.contains(uri_regex, na=False, case=True, regex=True)]
        if redirect_match.empty:
            print(f'test_substitution "{uri_test}" -> {uri_result}: '
                  + f'Missing redirect: no match for {uri_regex}')
        elif len(redirect_match) == 1:
            redirect_row = redirect_match.iloc[0]
            row_substituted = redirect_row[substituted_column]
            if row_substituted != uri_result:
                print(f'test_substitution "{uri_test}" -> {uri_result}:\n    '
                      + f'redirect_row[{substituted_column}]={row_substituted} != {uri_result}')
        else:
            print(f'test_substitution "{uri_test}" -> {uri_result}: '
                + f'{len(redirect_match)} redirects:\n{redirect_match}')

# Validation data
canonicalization_tests = [
    (r'/start', '/'),
    (r'/Page%28/_index.md%29', '/'),
    (r'/Page%28/technology/cisco-vpn-save-password-macos/index.md%29', '/technology/cisco-vpn-save-password-macos/'),
    (r'/articles/2011/02/18/time-machine-volume-uuid', '/articles/time-machine-volume-uuid/'),
    (r'/articles/2011/02/18/time-machine-volume-uuid/', '/articles/time-machine-volume-uuid/'),
    (r'/articles/2011/02/18/time-machine-volume-uuid/null', '/articles/time-machine-volume-uuid/'),
    (r'/articles/2011/02/18/time-machine-volume-uuid.html', '/articles/time-machine-volume-uuid/'),
    (r'/page/3', '/'),
    (r'/hints/windows/index', '/hints/windows/'),
]
test_substitution(df_canonicalized, canonicalization_tests, REQUEST_URI_CANONICAL)
# %%
# Apply transformation to account for relocations of entire sections
transformation_rules = [
    (r'^/(?:_media/)?(?:work/)?(?:publications/)?(dissertation|characterizing-networks|forwarding-paradigms).*', r'/research/\1/'),
    (r'^/(?:_media/)?(?:work/)?(publications/.*)', r'/research/\1'),
]

def transform_url(row):
    url = row[REQUEST_URI_CANONICAL]

    # Apply transformation rules
    for search_pattern, replacement in transformation_rules:
        if re.match(search_pattern, url):
            transformed_url = re.sub(search_pattern, replacement, url)
            return transformed_url

    return url

# Apply the function and create 'df_redirects'
df_transformed = df_canonicalized.copy()
df_transformed[REDIRECT_URI] = df_canonicalized.apply(transform_url, axis=1)
df_transformed[REDIRECT_STATUS] = HTTP_STATUS_REDIRECT
# Validation data
transformation_tests = [
    (r'/publications', '/research/publications/'),
    (r'/publications/', '/research/publications/'),
    (r'/publications/index', '/research/publications/'),
    (r'/forwarding-paradigms', '/research/forwarding-paradigms/'),
    (r'/characterizing-networks', '/research/characterizing-networks/'),
    (r'/publications/forwarding-paradigms', '/research/forwarding-paradigms/'),
    (r'/publications/characterizing-networks', '/research/characterizing-networks/'),
    (r'/publications/characterizing-networks.html', '/research/characterizing-networks/'),
    (r'/publications/forwarding-paradigms.html', '/research/forwarding-paradigms/'),
    (r'/publications/baumann_realistic-mobility-models_infocom07.pdf', '/research/publications/baumann_realistic-mobility-models_infocom07.pdf'),
    (r'/publications/dissertation', '/research/dissertation/'),
    (r'/publications/heimlicher_e2e-vs-hbh-transport_sigmetrics07.pdf', '/research/publications/heimlicher_e2e-vs-hbh-transport_sigmetrics07.pdf'),
    (r'/publications/heimlicher_globs_mobihoc10.pdf', '/research/publications/heimlicher_globs_mobihoc10.pdf'),
    (r'/_media/publications/heimlicher_globs_mobihoc10.pdf', '/research/publications/heimlicher_globs_mobihoc10.pdf'),
    (r'/_media/work/publications/heimlicher_transport-layer-revisited_comsware07.pdf', '/research/publications/heimlicher_transport-layer-revisited_comsware07.pdf'),
    (r'/_media/work/publications/heimlicher_saft_mass06.pdf', '/research/publications/heimlicher_saft_mass06.pdf'),
    (r'/_media/work/publications/heimlicher_partialpaths_infocom09.pdf', '/research/publications/heimlicher_partialpaths_infocom09.pdf'),
    (r'/_media/work/publications/baumann_realistic-mobility-models_infocom07.pdf', '/research/publications/baumann_realistic-mobility-models_infocom07.pdf'),
    (r'/_media/publications/', '/research/publications/'),
]
test_substitution(df_transformed, transformation_tests)
# %%
# Filter to create 'df_transformed'
df_redirects_accesslog = df_transformed[df_transformed[REDIRECT_URI].notnull()]
df_redirects_accesslog = df_redirects_accesslog[COLUMNS_ALL].reset_index()
df_redirects_accesslog.to_csv(OUTPUT_DIR / 'redirects_accesslog.csv', index=False)

# %%
# Get list of valid URLs and aliases from '_urls' and '_aliases' in Hugo's `public` directory
# File path of list of valid URLs
urls_path = HUGUO_OUTPUT_PUBLIC / '_urls'

processed_url_lines = []
with open(urls_path, 'r') as file:
    for line in file:
        # Split the line at the first unquoted '#'
        parts = line.split('#', 1)
        cleaned_line = parts[0].strip()  # Keep only the part before the '#'

        # Skip empty lines
        if cleaned_line:
            processed_url_lines.append(cleaned_line)

# Convert the processed lines into a DataFrame
df_hugo_valid_urls = pd.DataFrame(processed_url_lines, columns=[REQUEST_URI])

# File path to list of Hugo-generated alias mappings
aliases_path = HUGUO_OUTPUT_PUBLIC / '_aliases'

processed_alias_lines = []
with open(aliases_path, 'r') as file:
    for line in file:
        # Split the line at the first unquoted '#'
        parts = line.split('#', 1)
        cleaned_line = parts[0].strip()  # Keep only the part before the '#'

        # Skip empty lines
        if cleaned_line:
            processed_alias_lines.append(cleaned_line)

# Convert the processed lines into a DataFrame
df_hugo_alias_redirects = pd.DataFrame([line.split() for line in processed_alias_lines],
                                       columns=[REQUEST_URI, REDIRECT_URI, REDIRECT_STATUS])

# %%
# Merge Hugo-generated redirects with canonicalization redirects
df_merged_redirects = pd.DataFrame(columns=COLUMNS_ALL)
merged_redirects_list = []

for index, row in df_redirects_accesslog.iterrows():

    # Default to no redirect, i.e., column REDIRECT_URI is `None` and status is `200`
    new_row = {
        REQUEST_URI: row[REQUEST_URI],
        REQUEST_URI_CANONICAL: row[REQUEST_URI_CANONICAL],
        REDIRECT_URI: None,
        REDIRECT_STATUS: HTTP_STATUS_OK,
        ACCESS_COUNT: row[ACCESS_COUNT],
        LAST_ACCESS: row[LAST_ACCESS],
        STATUS_CODE: row[STATUS_CODE],
    }

    # 1. Determine if the URL we try to redirect is a valid page, in which case it should not be redirected
    url_match = df_hugo_valid_urls[df_hugo_valid_urls[REQUEST_URI] == row[REQUEST_URI]]
    if url_match.empty:

        #
        # The URL in the REQUEST_URI column is not a valid page URL
        # It still might be a valid URL for another media type
        #

        # 2. Determine if the canonical version of the URL is a valid page URL
        # If so, the URL should be redirected to its canonical version
        canonical_match = df_hugo_valid_urls[df_hugo_valid_urls[REQUEST_URI] == row[REQUEST_URI_CANONICAL]]
        if not canonical_match.empty:
            # The URL in the REQUEST_URI_CANONICAL column is a valid URL and we should redirect to it
            new_row[REDIRECT_STATUS] = HTTP_STATUS_REDIRECT
            new_row[REDIRECT_URI] = row[REQUEST_URI_CANONICAL]
        else:
            # Check if there is a redirect mapping from an alias in `df_hugo_alias_redirects` for the canonical URL
            alias_match = df_hugo_alias_redirects[df_hugo_alias_redirects[REQUEST_URI] == row[REQUEST_URI]]
            if not alias_match.empty:
                new_row[REDIRECT_STATUS] = HTTP_STATUS_REDIRECT
                new_row[REDIRECT_URI] = alias_match.iloc[0][REDIRECT_URI]  # First matching record's Redirect URL
            else:
                # 3. Determine if the current redirect URL is a valid URL and the original URL should be redirected
                redirect_match = df_hugo_valid_urls[df_hugo_valid_urls[REQUEST_URI] == row[REDIRECT_URI]]
                if not redirect_match.empty:
                    #  Current redirect URL is valid as the URL exists in df_hugo_valid_urls
                    new_row[REDIRECT_STATUS] = HTTP_STATUS_REDIRECT
                    new_row[REDIRECT_URI] = row[REDIRECT_URI]
                else:
                    # Check if there is a redirect mapping from an alias in `df_hugo_alias_redirects` for the canonical URL
                    canonical_alias_match = df_hugo_alias_redirects[df_hugo_alias_redirects[REQUEST_URI] == row[REQUEST_URI_CANONICAL]]
                    if not canonical_alias_match.empty:
                        new_row[REDIRECT_STATUS] = HTTP_STATUS_REDIRECT
                        new_row[REDIRECT_URI] = canonical_alias_match.iloc[0][REDIRECT_URI]  # First matching record's Redirect URL
                    else:
                        redirect_alias_match = df_hugo_alias_redirects[df_hugo_alias_redirects[REQUEST_URI] == row[REDIRECT_URI]]
                        if not redirect_alias_match.empty:
                            new_row[REDIRECT_STATUS] = HTTP_STATUS_REDIRECT
                            new_row[REDIRECT_URI] = redirect_alias_match.iloc[0][REDIRECT_URI]  # First matching record's Redirect URL
                        else:
                            # No page to redirect to found.
                            # If the URL corresponds to a file, we blindly redirect
                            if (re.match(r'.*\.[a-z0-9]+$', row[REQUEST_URI_CANONICAL], flags=re.IGNORECASE)
                                and row[REDIRECT_URI] != row[REQUEST_URI]
                                ):
                                new_row[REDIRECT_STATUS] = HTTP_STATUS_REDIRECT
                                new_row[REDIRECT_URI] = row[REDIRECT_URI]
                            else:
                                # Redirect to the canonical URL as all the default rules below are based on canonical URLs
                                new_row[REDIRECT_STATUS] = HTTP_STATUS_NOT_FOUND
                                new_row[REDIRECT_URI] = row[REQUEST_URI_CANONICAL]

    # Append the new row to the list
    merged_redirects_list.append(new_row)

# Convert the list of dictionaries to a DataFrame
df_merged_redirects = pd.DataFrame(merged_redirects_list)
df_merged_redirects
test_substitution(df_merged_redirects, transformation_tests)


# %%
# Redirect a selection of obsoleted URLs to the most relevant category or section to avoid 404 errors
default_rules = [
    (r'^/private/.*', r'/about/'),
    (r'^/articles.*time-machine-volume-uuid.*', r'/technology/time-machine-volume-uuid/'),
    (r'^/articles.*time-machine.*', r'/technology/time-machine-inherit-backup-using-tmutil/'),
    (r'^/public/tips/macosx/.*', r'/technology/'),
    (r'^/(?:work|software)/.*', r'/technology/'),
    (r'^/hints/macosx(?:/server)?.*', r'/technology/'),
    (r'^/hints.*', r'/technology/'),
    (r'^/tags/(?:ios|ipad|matlab|nginx|perl|programming|time-machine).*', r'/technology/'),
    (r'^/articles/os-x.*', r'/technology/'),
    (r'^/articles/style.*', r'/digitization/'),
    (r'^/articles.*', r'/technology/'),
]

def default_url(row):
    redirect_uri = row[REDIRECT_URI]
    redirect_status = row[REDIRECT_STATUS]

    if redirect_status == HTTP_STATUS_NOT_FOUND:
        canonical_uri = row[REQUEST_URI_CANONICAL]

        # Apply transformation rules
        for search_pattern, replacement in default_rules:
            if re.match(search_pattern, canonical_uri):
                redirect_uri = re.sub(search_pattern, replacement, canonical_uri)
                redirect_status = HTTP_STATUS_REDIRECT
                return pd.Series([redirect_uri, redirect_status])

    return pd.Series([redirect_uri, redirect_status])

# Apply the function and create 'df_redirects_raw'
df_merged_defaulted_redirects = df_merged_redirects.copy()
df_merged_defaulted_redirects[[REDIRECT_URI, REDIRECT_STATUS]] = df_merged_defaulted_redirects.apply(default_url,
                                                                   axis=1, result_type='expand')
# Ensure that column `Redirect Status` contains only integers
df_merged_defaulted_redirects[REDIRECT_STATUS] = df_merged_defaulted_redirects[REDIRECT_STATUS].astype(int)
# diff_df(df_merged_redirects, df_merged_defaulted_redirects)
valid_redirects_mask = df_merged_defaulted_redirects[REDIRECT_STATUS] == HTTP_STATUS_REDIRECT
df_redirects_valid = df_merged_defaulted_redirects[valid_redirects_mask]

default_tests = [
    (r'/tags/ipad/', r'/technology/'),
    (r'/tags/matlab/', r'/technology/'),
    (r'/tags/time-machine/', r'/technology/'),
    (r'/tags/performance/index.xml', r'/tags/performance/'),
]
test_substitution(df_redirects_valid, default_tests)

# %%
# Validate redirects against historical URLs

validation_file = ROOT_DIR / 'validation' / 'redirects_historical.csv'

def validate_redirects(df_redirects, csv_file):
    df_validation = pd.read_csv(csv_file)

    mismatches = []
    for index, test_row in df_validation.iterrows():
        error = None
        # Get all matching records from the redirects data frame
        redirect_match = df_redirects[
            df_redirects[REQUEST_URI].str.contains(r'^' + test_row[REQUEST_URI] + '$',
                                                                na=False, case=True, regex=True)
        ]

        if test_row[REDIRECT_STATUS] == HTTP_STATUS_OK:
            # Validate that there is no redirect for this URL in df_redirects
            if not redirect_match.empty:
                # Get the first row from the matching ones
                redirect_row = redirect_match.iloc[0]
                error = (f"Unwanted redirect: uri {test_row[REQUEST_URI]} has status {test_row[REDIRECT_STATUS]}\n"
                        + f"unwanted: {redirect_row[REQUEST_URI]} -> {redirect_row[REDIRECT_URI]} {redirect_row[REDIRECT_STATUS]}")
        else:
            # Validate that there a redirect for this URL in df_redirects and it is correct
            if not redirect_match.empty:
                # Get the first row from the matching ones
                redirect_row = redirect_match.iloc[0]
                if (redirect_row[REDIRECT_URI] != test_row[REDIRECT_URI] or
                        redirect_row[REDIRECT_STATUS] != test_row[REDIRECT_STATUS]):
                    error = (f"Wrong redirect {redirect_row[REQUEST_URI]} -> {redirect_row[REDIRECT_URI]} {redirect_row[REDIRECT_STATUS]}:\n    "
                        + f"expected: {test_row[REQUEST_URI]} -> {test_row[REDIRECT_URI]} {test_row[REDIRECT_STATUS]}")
            else:
                error = (f"Missing redirect {test_row[REQUEST_URI]} -> {test_row[REDIRECT_URI]} {test_row[REDIRECT_STATUS]}")

        if error:
            print(error)
            mismatches.append({"test": test_row, "redirect": redirect_match})

    return mismatches

mismatched_redirects = validate_redirects(df_redirects_valid, validation_file)
# %%
# Output valid redirects to CSV file and recent and frequent subset for Hugo as JSON
# Write the DataFrame to a CSV file
df_redirects_valid.to_csv(OUTPUT_DIR / 'redirects.csv', index=False)
df_redirects_valid

# Output valid redirects to Hugo `data` directory
# Prepare data frame for output
df_redirects_recent = df_redirects_valid.copy()

# Accessed since the year 2020 or later...
df_redirects_recent = df_redirects_recent[df_redirects_recent[LAST_ACCESS].dt.year >= 2021]
# ... at least 10 times
df_redirects_recent_frequent = df_redirects_recent[df_redirects_recent[ACCESS_COUNT] > 10]

df_redirects_hugo = df_redirects_recent_frequent[[REQUEST_URI, REDIRECT_URI, REDIRECT_STATUS]]
df_redirects_hugo = df_redirects_hugo.rename(columns={REQUEST_URI: 'path',
                                                      REDIRECT_URI: 'target',
                                                      REDIRECT_STATUS: 'status'})
df_redirects_hugo = df_redirects_hugo.sort_values(by='path',
                                                  key=lambda x: x.str.lower(), ascending=True)
# Write the DataFrame to a CSV file for manual inspection (easier to read than JSON)
df_redirects_hugo.to_csv(OUTPUT_DIR / 'hugo_data_redirects.csv', index=False)

# Write the DataFrame to a JSON file in Hugo's `data` directory to enable
# Hugo to generate the final `_redirects` file via the template `layouts/index.redir`
df_redirects_hugo.to_json(HUGO_DATA_DIR / 'redirects.json', orient='records')

# Output records that lead to invalid URLs to CSV file
invalid_redirects_mask = df_redirects_recent_frequent[REDIRECT_STATUS] == HTTP_STATUS_NOT_FOUND
df_redirects_invalid = df_redirects_recent_frequent[invalid_redirects_mask]

# Write the DataFrame to a CSV file
df_redirects_invalid.to_csv(OUTPUT_DIR / 'redirects_invalid.csv', index=False)

# Output records that have URLs and must not be redirected to CSV file
url_was_valid_mask = df_redirects_recent_frequent[STATUS_CODE] == HTTP_STATUS_OK
url_is_valid_mask = df_redirects_recent_frequent[REDIRECT_STATUS] == HTTP_STATUS_OK
unwanted_redirects_mask = url_was_valid_mask & url_is_valid_mask
df_redirects_unwanted = df_redirects_recent_frequent[unwanted_redirects_mask]

# Write the DataFrame to a CSV file
df_redirects_unwanted.to_csv(OUTPUT_DIR / 'redirects_unwanted.csv', index=False)

# Get invalid redirects for validation
# validation_mask = df_redirects_recent_frequent[REQUEST_URI_CANONICAL].str.contains(r'^/[-a-z0-9._]{3,}/$',
#                                                         na=False, case=False, regex=True)
# df_redirects_recent_frequent[invalid_redirects_mask & validation_mask]

df_redirects_recent_frequent

# print("- " + "\n- ".join(df_redirects_recent_frequent[invalid_redirects_mask & validation_mask][REDIRECT_URI].to_list()))

# %%
