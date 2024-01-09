from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource

df_redirects_2018_10 = df_redirects[
    (df_redirects['Last Access'].dt.year >= 2018) &      # Last Access is in the year 2018 or later
    (df_redirects['Access Count'] > 10)                  # Total Access Count is greater than 10
]

df_redirects_2018_10.to_csv('accesslog_redirects_after2018_min10.csv', index=False)
df_redirects_2018_10

# Enable the output of bokeh plots in Jupyter Notebook
output_notebook()

source_df = df_redirects_2018_10

# Create a ColumnDataSource from the top 10 data
source = ColumnDataSource(data=source_df)

# Create the figure
p = figure(y_range=source_df['URL'], height=1600, width=800, title="Top 10 Frequently Accessed URLs with Status Code 301", tools="pan,box_zoom,reset")

# Add horizontal bar plot
p.hbar(y='URL', right='Total Access Count', source=source, height=0.4)

# Add labels
p.xaxis.axis_label = 'Number of Accesses'
p.yaxis.axis_label = 'URLs'

# Show the plot
show(p)
# %%
# Get all access to PHP files, ignoring invalid URLs

# Ignore invalid URLs
# invalid_urls_pattern = (r'^/+(?:[?_]+'
#     + r'|db|upload|include|mindmeld|mods|module|lib|package|page|ops|sql|shell|inc|feed|media|plus'
#     + r'|data|tmp|index|vendor|sites|stream|lock|scripts|40|export|root|license|style|java'
#     + r'|fw|image|img|layout|lang|mail'
#     + r'|s_|photo|wp[^a-z]|plug|pod|defa|bu|mt|core|theme'
#     + r'|xl|indox|pma|xx|tp|.well-known'
#     + r'|[^/]+\.php'
#     + r')'
#     + r'|laravel|lufix|beence|mxbb|mygallery|ossigeno|phorum|promocms|agsearch|kcfinder|n0way|explore'
#     + r'|assetmanager|assets|css|js|mybic|appserv|footer|nuclearbb|mser|creativecontact|betablock|downstat|docebo|dm-album|heimlicher|ispirit|logs|code|privilege'
#     + r'|wp-|adm|_fragment|wchat|phpstorm|server/php|phpinfo|phpunit|vtiger|fck|config|echo|system|template|elseif|password|tool'
#     + r'|xmlrpc|public_html|install|cgi|local-bin|register|test|phpmyadmin|myadmin|myaccount|atutor'
#     + r'|b2-tools|magmi|news|frame|mod_|cache|bridge|moteur|music|shop|script|process|skin|source'
#     + r'|class|alert|common|wapchat|ytb|recording|address|component|client|web|wsk|content|bins|public|upload|compteur|control|convert|product|runtime|dump|dialog|guestbook|gaestebuch|gastenboek|gb'
#     + r'|adaptcms|bpnews|user|gemini|snippetmaster|download|logging|contenido|modules|include|widget|squery|don3|templates|gallery|adodb|path|ajax|amazon|akarru|belegungsplan|bemarket|bigace'
#     + r'|(?:index|z|doc|wp|info|editor|dropdown|alfa|up|about|wso|moon|pipe|data|defaul1|team|setup|by|byp|cp|customize|default|md5|petx|apps|elfinder|timeclock|header|donation|links|search|viar|application|core'
#     + r'|edit-comments|fm|gecko|member|home|init|lufi|ws|log|plugins|repeater|books|action|util|article-raw|radio|elrekt|moduless|forum|mytag_js|reg|sky|protection|ee|auth|upl|google|marijuana|view|pollvote|popup_window|port|mysave|simple|browser|router|wiki|login|ups|olux|legion|sym|symmlink|error|term|tesla|lalala|leet|lydia|mar|/[a-z]|/[0-9]+)[^a-z]?\.php'
#     + r'|\bphp[^?]+'
# )
# # invalid_urls_pattern
# invalid_urls_mask = df['URL'].str.contains(invalid_urls_pattern, na=False, case=False)
# df_valid = df[~invalid_urls_mask]

# %%
# # Length of continuous sequence of URL-encoded characters
# encoded_seq_len = 1

# # Regular expression for URL escape sequences
# escape_seq_regex = r'(?:%[0-9A-Fa-f]{2}){' + f"{encoded_seq_len},{encoded_seq_len}" + r'}'

# # Function to find all escape sequences in a URL
# def find_escape_sequences(url):
#     return [seq.upper() for seq in re.findall(escape_seq_regex, url)]

# # Data structure to store the escape sequences, counts, and last access
# escape_data = defaultdict(lambda: {'count': 0, 'last_access': None})

# # Iterate over each row in the DataFrame
# for index, row in df.iterrows():
#     escape_sequences = find_escape_sequences(row['URL'])
#     for seq_upper in escape_sequences:
#         escape_data[seq_upper]['count'] += 1
#         if not escape_data[seq_upper]['last_access'] or row['Last Access'] > escape_data[seq_upper]['last_access']:
#             escape_data[seq_upper]['last_access'] = row['Last Access']

# # Convert the escape data to a DataFrame and include the decoded character
# df_escape_sequences = pd.DataFrame([
#     {
#         'Escape Sequence': seq,
#         'Decoded Characters': unquote(seq),
#         'Total Access Count': data['count'],
#         'Last Access': data['last_access']
#     }
#     for seq, data in escape_data.items()
# ])

# df_escape_sequences.sort_values(by='Total Access Count', ascending=False, inplace=True)
# covered_lines = set()
# selected_sequences = set()

# # Iterate over the sorted escape sequences DataFrame
# for index, row in df_escape_sequences.iterrows():
#     seq = row['Escape Sequence']

#     # Find all lines in the original DataFrame that contain this sequence
#     matching_lines = {idx for idx, url in enumerate(df['URL']) if seq in url}

#     # Check if this sequence covers new lines
#     new_lines = matching_lines - covered_lines
#     if new_lines:
#         # This sequence covers new lines, add it to the selected sequences
#         selected_sequences.add(seq)
#         covered_lines.update(new_lines)

#     # Check if all lines are covered
#     if len(covered_lines) == len(df):
#         break

# # selected_sequences now contains the minimal set of sequences
# print(selected_sequences)

# %%
# Get all access to PHP files, ignoring invalid URLs

# Ignore invalid URLs
# invalid_urls_pattern = (r'^/+(?:[?_]+'
#     + r'|db|upload|include|mindmeld|mods|module|lib|package|page|ops|sql|shell|inc|feed|media|plus'
#     + r'|data|tmp|index|vendor|sites|stream|lock|scripts|40|export|root|license|style|java'
#     + r'|fw|image|img|layout|lang|mail'
#     + r'|s_|photo|wp[^a-z]|plug|pod|defa|bu|mt|core|theme'
#     + r'|xl|indox|pma|xx|tp|.well-known'
#     + r'|[^/]+\.php'
#     + r')'
#     + r'|laravel|lufix|beence|mxbb|mygallery|ossigeno|phorum|promocms|agsearch|kcfinder|n0way|explore'
#     + r'|assetmanager|assets|css|js|mybic|appserv|footer|nuclearbb|mser|creativecontact|betablock|downstat|docebo|dm-album|heimlicher|ispirit|logs|code|privilege'
#     + r'|wp-|adm|_fragment|wchat|phpstorm|server/php|phpinfo|phpunit|vtiger|fck|config|echo|system|template|elseif|password|tool'
#     + r'|xmlrpc|public_html|install|cgi|local-bin|register|test|phpmyadmin|myadmin|myaccount|atutor'
#     + r'|b2-tools|magmi|news|frame|mod_|cache|bridge|moteur|music|shop|script|process|skin|source'
#     + r'|class|alert|common|wapchat|ytb|recording|address|component|client|web|wsk|content|bins|public|upload|compteur|control|convert|product|runtime|dump|dialog|guestbook|gaestebuch|gastenboek|gb'
#     + r'|adaptcms|bpnews|user|gemini|snippetmaster|download|logging|contenido|modules|include|widget|squery|don3|templates|gallery|adodb|path|ajax|amazon|akarru|belegungsplan|bemarket|bigace'
#     + r'|(?:index|z|doc|wp|info|editor|dropdown|alfa|up|about|wso|moon|pipe|data|defaul1|team|setup|by|byp|cp|customize|default|md5|petx|apps|elfinder|timeclock|header|donation|links|search|viar|application|core'
#     + r'|edit-comments|fm|gecko|member|home|init|lufi|ws|log|plugins|repeater|books|action|util|article-raw|radio|elrekt|moduless|forum|mytag_js|reg|sky|protection|ee|auth|upl|google|marijuana|view|pollvote|popup_window|port|mysave|simple|browser|router|wiki|login|ups|olux|legion|sym|symmlink|error|term|tesla|lalala|leet|lydia|mar|/[a-z]|/[0-9]+)[^a-z]?\.php'
#     + r'|\bphp[^?]+'
# )
# # invalid_urls_pattern
# invalid_urls_mask = df['URL'].str.contains(invalid_urls_pattern, na=False, case=False)
# df_valid = df[~invalid_urls_mask]
