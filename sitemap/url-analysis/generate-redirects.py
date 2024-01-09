# %%
# Read data from aggregated nginx access log file
from pathlib import Path
import re
from urllib.parse import unquote, urlparse
from collections import defaultdict
import pandas as pd

# Dmains
ORIGINAL_DOMAIN = 'heimlicher.com'
ORIGINAL_HOST_MATCH_RE = r'(?:[-a-z]+\.)*' + re.escape(ORIGINAL_DOMAIN)

# Column names
REQUEST_URI = 'URI'
REQUEST_URI_WITHOUT_QUERY = 'URI without query'
REQUEST_URI_CANONICAL = 'Canonical'
LAST_ACCESS = 'Last'
ACCESS_COUNT = 'Count'
STATUS_CODE = 'Status'
REDIRECT_URI = 'Redirect URI'
REDIRECT_STATUS = 'Redirect status'

COLUMNS_INPUT = [REQUEST_URI, ACCESS_COUNT, LAST_ACCESS, STATUS_CODE]
COLUMNS_INPUT_CANONICAL = [REQUEST_URI, REQUEST_URI_CANONICAL, ACCESS_COUNT, LAST_ACCESS, STATUS_CODE]
COLUMNS_ALL = [REQUEST_URI, REQUEST_URI_CANONICAL, REDIRECT_URI, REDIRECT_STATUS, ACCESS_COUNT, LAST_ACCESS, STATUS_CODE]

# Directories
ROOT_DIR = Path(__file__).absolute().parent
INPUT_DIR = ROOT_DIR / "input"
OUTPUT_DIR = ROOT_DIR / "output"
HUGO_PROJECT_DIR = ROOT_DIR.parent.parent
HUGO_DATA_DIR = HUGO_PROJECT_DIR / "data"
HUGUO_OUTPUT_PUBLIC = HUGO_PROJECT_DIR / "output" / "serve" / "devel"

HTTP_STATUS_OK = 200
HTTP_STATUS_REDIRECT = 301
HTTP_STATUS_NOT_FOUND = 404

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
malicous_regex = r"^/data|^/api|&amp|&quot|\\x22|select*|/RK=0|/RS=\^|'x'|\+\+\+\+|2wCEAAgGBgcGB|vWfM6kbCUIv|fa3c615d773|iVBORw0KGgo"
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
df_cleaned

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
df_aggregated

# %%
# Add a column that contains a canonicalized form of the URL
canonicalization_rules = [
    # (r'^https?://' + ORIGINAL_HOST_MATCH_RE + r'(?::[0-9]+)?(/(?:[^/" ]+/)*[^/" ]*)', r'^https?://' + ORIGINAL_HOST_MATCH_RE + r'(?::[0-9]+)?(/(?:[^/" ]+/)*[^/" ]*)$', r'\1'),
    (r'^/Page(?:[(]|%28)(.*)(?:(/[^./]*)|(?:/_?index\.md))(?:[)]|%29)$', r'^/Page(?:[(]|%28)(.*)(?:(/[^./]*)|(?:/_?index\.md))(?:[)]|%29)$', r'\1\2/'),
    (r'^/articles/[0-9]{4}', r'^(/articles/)(?:[0-9]{4}/[0-9]{2}/[0-9]{2}/)([^/]+).*$', r'\1\2/'),
    (r'.*/(?:atom|index)', r'(.*?/)(?:atom|index).*', r'\1'),
    (r'.*/page/[1-9]*/?$', r'(.*?/)page/[1-9].*', r'\1'),
    (r'^/hints', r'_', r'-'),
    (r'.*\.html', r'(.*?)(?:/index)?\.html.*', r'\1/'),
    (r'^(.*/[^./]+)$', r'(^.*/[^./]+)$', r'\1/'),
]

def canonicalize_url(row):
    url = row[REQUEST_URI]
    canonical_url = url
    # Apply all canonicalization rules in sequence
    for pattern, search_pattern, replacement in canonicalization_rules:
        if re.match(pattern, canonical_url):
            canonical_url = re.sub(search_pattern, replacement, canonical_url)

    return canonical_url

# Apply the function and create 'df_canonicalized'
df_canonicalized = df_aggregated.copy()
df_canonicalized[REQUEST_URI_CANONICAL] = df_aggregated.apply(canonicalize_url, axis=1)
df_canonicalized = df_canonicalized[COLUMNS_INPUT_CANONICAL].reset_index()
df_canonicalized

# %%
# Apply transformation to account for relocations of entire sections
transformation_rules = [
    (r'^/publications/.*', r'^(/publications/.*)', r'/research\1'),
    (r'^/(?:publications/)?(dissertation|characterizing-networks|forwarding-paradigms)', r'^/(?:publications/)?(dissertation|characterizing-networks|forwarding-paradigms)', r'/research\1'),
    # (r'^/hints', r'^/hints(?:/[^./]+)*/([^./]+)/*$', r'/articles/\1/'),
]

def transform_url(row):
    url = row[REQUEST_URI_CANONICAL]

    # Apply transformation rules
    for pattern, search_pattern, replacement in transformation_rules:
        if re.match(pattern, url):
            url = re.sub(search_pattern, replacement, url)

    return url

# Apply the function and create 'df_redirects'
df_redirects = df_canonicalized.copy()
df_redirects[REDIRECT_URI] = df_canonicalized.apply(transform_url, axis=1)
df_redirects[REDIRECT_STATUS] = HTTP_STATUS_REDIRECT

# Filter to create 'df_redirects'
df_redirects = df_redirects[df_redirects[REDIRECT_URI].notnull()]
df_redirects = df_redirects[COLUMNS_ALL].reset_index()
df_redirects.to_csv(OUTPUT_DIR / 'accesslog_redirects.csv', index=False)
df_redirects

# %%
# Get list of valid URLs and aliases from Hugo `public` directory
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

for index, row in df_redirects.iterrows():

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

        # 3. Determine if the current redirect URL is a valid URL and the original URL should be redirected
        redirect_match = df_hugo_valid_urls[df_hugo_valid_urls[REQUEST_URI] == row[REDIRECT_URI]]
        if not redirect_match.empty:
            #  Current redirect URL is valid as the URL exists in df_hugo_valid_urls
            new_row[REDIRECT_STATUS] = HTTP_STATUS_REDIRECT
            new_row[REDIRECT_URI] = row[REDIRECT_URI]
        else:
            # Check if there is a redirect mapping from an alias in `df_hugo_alias_redirects` for the REDIRECT_URI
            redirect_alias_match = df_hugo_alias_redirects[df_hugo_alias_redirects[REQUEST_URI] == row[REDIRECT_URI]]
            if not redirect_alias_match.empty:
                new_row[REDIRECT_STATUS] = HTTP_STATUS_REDIRECT
                new_row[REDIRECT_URI] = redirect_alias_match.iloc[0][REDIRECT_URI]  # First matching record's Redirect URL
            else:
                # No page to redirect to found
                # Since the URL may still be valid, for example referring to a PDF,
                # we add the canonicalized REDIRECT_URI if it differs from the REQUEST_URI
                # but with a status of 'not found' as we are unable to determine if the redirect URL is valid
                new_row[REDIRECT_URI] = row[REQUEST_URI_CANONICAL]
                new_row[REDIRECT_STATUS] = HTTP_STATUS_NOT_FOUND

    # Append the new row to the list
    merged_redirects_list.append(new_row)

# Convert the list of dictionaries to a DataFrame
df_merged_redirects = pd.DataFrame(merged_redirects_list)
df_merged_redirects

hints_mask = df_merged_redirects[REQUEST_URI_CANONICAL].str.contains(r'^/hints/perl',
                                                        na=False, case=False, regex=True)
df_merged_redirects[hints_mask]

# %%
# Redirect a selection nof outdated URLs to the most relevant category or section to avoid 404 errors
default_rules = [
    (r'^/hints/macosx.*', r'^/hints/macosx(?:/server)?.*', r'/categories/macos/'),
    (r'^/hints.*', r'^/hints.*', r'/technology/'),
]

def default_url(row):
    redirect_uri = row[REDIRECT_URI]
    redirect_status = row[REDIRECT_STATUS]

    if redirect_status == HTTP_STATUS_NOT_FOUND:
        canonical_uri = row[REQUEST_URI_CANONICAL]

        # Apply transformation rules
        for pattern, search_pattern, replacement in default_rules:
            if re.match(pattern, canonical_uri):
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
df_redirects = df_merged_defaulted_redirects.copy()
hints_mask = df_redirects[REQUEST_URI_CANONICAL].str.contains(r'^/hints/perl',
                                                        na=False, case=False, regex=True)
df_redirects[hints_mask]

# %%
# Output valid redirects for Hugo as JSON
valid_redirects_mask = df_redirects[REDIRECT_STATUS] == HTTP_STATUS_REDIRECT

# Output valid redirects to CSV file
df_redirects_valid = df_redirects[valid_redirects_mask]

# Write the DataFrame to a CSV file
df_redirects_valid.to_csv(OUTPUT_DIR / 'redirects.csv', index=False)
df_redirects_valid

# Output valid redirects to Hugo `data` directory
# Prepare data frame for output
df_redirects_hugo = df_redirects_valid.copy()
df_redirects_hugo = df_redirects_hugo[[REQUEST_URI, REDIRECT_URI, REDIRECT_STATUS]]
df_redirects_hugo = df_redirects_hugo.rename(columns={REQUEST_URI: 'path',
                                                      REDIRECT_URI: 'target',
                                                      REDIRECT_STATUS: 'status'})
df_redirects_hugo = df_redirects_hugo.sort_values(by='path',
                                                  key=lambda x: x.str.lower(), ascending=True)
# Write the DataFrame to a CSV file for manual inspection (easier to read than JSON)
df_redirects_hugo.to_csv(OUTPUT_DIR / 'hugo_data_redirects.csv', index=False)

# Write the DataFrame to a JSON file in Hugo's `data` directory to enable
# Hugo to generate the final `_redirects` file via the template `layouts/index.redir`
df_redirects_hugo.to_json(HUGO_DATA_DIR / 'redirects.json', orient='records', lines=False)
df_redirects_hugo

# %%

# %%
# Output records that lead to invalid URLs to CSV file
invalid_redirects_mask = df_redirects[REDIRECT_STATUS] == HTTP_STATUS_NOT_FOUND
df_redirects_invalid = df_redirects[invalid_redirects_mask]

# Write the DataFrame to a CSV file
df_redirects_invalid.to_csv(OUTPUT_DIR / 'redirects_invalid.csv', index=False)
df_redirects_invalid
# %%
# Output records that have URLs and must not be redirected to CSV file
url_was_valid_mask = df_redirects[STATUS_CODE] == HTTP_STATUS_OK
url_is_valid_mask = df_redirects[REDIRECT_STATUS] == HTTP_STATUS_OK
unwanted_redirects_mask = url_was_valid_mask & url_is_valid_mask
df_redirects_unwanted = df_redirects[unwanted_redirects_mask]

# Write the DataFrame to a CSV file
df_redirects_unwanted.to_csv(OUTPUT_DIR / 'redirects_unwanted.csv', index=False)
df_redirects_unwanted

# %%
# Get invalid redirects that begin with `/articles`
articles_mask = df_redirects[REDIRECT_URI].str.contains(r'^/articles/[-a-z0-9._]{3,}/$',
                                                        na=False, case=False, regex=True)
df_redirects_invalid_articles = df_redirects[invalid_redirects_mask & articles_mask]
df_redirects_invalid_articles
# %%
# Get invalid redirects that do NOT begin with `/articles`
df_redirects[invalid_redirects_mask & ~articles_mask].sort_values([ACCESS_COUNT, LAST_ACCESS],
                                                                  ascending=[False,False])

# %%
