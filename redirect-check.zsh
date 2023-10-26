#!/usr/bin/env zsh
#
#
base=${1:='https://simon.heimlicher.com'}

function get_uri() {
    local url=$base$uri
    local ret=$(curl -X GET -s -I "$url" 2>&1)
    # print "BEGIN\n$ret\nEND"
    # FIXME: Need to remove trailing  to avoid funny things from happening when output to shell
    local http_status=$(print $ret | sed -E -n "s!^(HTTP/[1-9]+) ([0-9]+).*!\2[\1]!p")
    local redirect_target=$(print $ret | sed -E -n "s!^location: $base([^[:space:]]+)!\1!p")
    if [[ -z $redirect_target ]]; then
        redirect_target=$(print $ret | sed -E -n "s!^location: ([^[:space:]]+)!\1!p")
    fi
    # print "http_status: '$http_status'"
    # print "redirect_target: '$redirect_target'"
    if [[ $http_status == 200* ]]; then
        print "OK:       $http_status $uri"
    elif [[ $http_status == 301* ]]; then
        print "REDIRECT: $http_status $uri --> $redirect_target"
    else
        # print FAIL: $url | rg 'FAIL:'
        print "FAIL:     $http_status $uri" | rg 'FAIL:'
    fi
}

# date='2000/00/99'
# for slug ('cisco-vpn-10.6.0-3' 'multiple-email' 'multiple-identities-mail' 'non-existing'); do
#     for p ("$date/$slug" "$date/$slug/" "$slug" "$slug/"); do
#         uri="/articles/$p"
#         get_uri $uri
#     done
# done

prior_urls=(
    /
    /about
    /about/
    /articles
    /articles/
    /articles/capitalization-title-headings-preferences/
    /articles/capitalization/
    /articles/cisco-vpn-10.6.0-3/
    /articles/cisco-vpn-save-password-macos/
    /articles/cisco-vpn/
    /articles/comodo-ssl-certificate-with-nginx/
    /articles/disable-recent-items/
    /articles/disk-failure/
    /articles/file_vault_2/
    /articles/fix-cisco-vpn-disconnections-mac-os-x-10.6.0-10.6.3/
    /articles/multiple-email/
    /articles/multiple-from-email-addresses-apple-mail-lion/
    /articles/multiple-from-email-addresses-ios-iphone-ipad/
    /articles/multiple-identities-mail/
    /articles/okrs-vs-performance-management/
    /articles/powerful-patty-mccord/
    /articles/private-browsing/
    /articles/smtp-smarthost/
    /articles/time-machine-inherit-backup-using-tmutil/
    /articles/time-machine-readonly/
    /articles/time-machine-volume-uuid/
    /articles/turn-the-ship-around-l-david-marquet/
    /articles/turn-the-ship-around/
    /articles/why-okr-objectives-key-results-already-have-goals/
    /articles/why-okrs-already-have-goals/
    /categories/
    /categories/book/
    /categories/communication/
    /categories/leadership/
    /categories/macos/
    /categories/management/
    /categories/methodology/
    /de/categories/
    /de/categories/book/
    /de/categories/communication/
    /de/categories/leadership/
    /de/categories/macos/
    /de/categories/management/
    /de/categories/methodology/
    /_error/
    /_error/401/
    /_error/403/
    /_error/404/
    /_error/500/
    /_error/504/
    /hints/ipad/multiple-email/
    /hints/macosx/cisco_vpn-10.6.0-3/
    /hints/macosx/cisco_vpn/
    /hints/macosx/disable_recent_items/
    /hints/macosx/disk-failure/
    /hints/macosx/file_vault_2/
    /hints/macosx/multiple_identities_mail/
    /hints/macosx/private_browsing/
    /hints/macosx/time-machine-readonly/
    /hints/macosx/time-machine-volume-uuid/
    /hints/style/capitalization/
    /home/
    /home/about/
    /research/
    /research/characterizing-networks/
    /research/dissertation/
    /research/forwarding-paradigms/
    /research/publications/
    /series/
    /series/leadership/
    /series/okr/
    /tags/
    /tags/capitalization/
    /tags/cisco/
    /tags/cleanup/
    /tags/communication/
    /tags/leadership/
    /tags/macos/
    /tags/okr/
    /tags/performance/
    /tags/privacy/
    /tags/talent/
    /tags/vpn/
    /tags/writing/

    /de/organizational-transformation/
    /de/transformation/organizational-transformation-objectives-key-results-okr-performance-management/
    /articles/2011/09/26/nstat-lookup-entry-failed-2
    /tags/windows/
    /tags/iphone/
    /articles/2012/05/02/acm-template-with-basic-tex-live/
    /categories/latex/
    /categories/windows/
    /articles/2012/02/01/jekyll-directory-listing
    /articles/2008/03/20/kdcmond
    /articles/2011/07/23/file-vault-2/
    /tags/latex/
    /work/
    /tags/ipad/
    /articles/2011/03/17/cisco-vpn-10.6
    /categories/programming/
    /articles/share-media/
    /categories/style/
    /articles/okrs-vs.-performance-management/
    /categories/linux
    /articles/2010/03/04/quicklook/
    /Page%28/_index.md%29
    /Page%28/technology/fix-cisco-vpn-disconnections-mac-os-x-10.6.0-10.6.3/index.md%29
    /Page%28/tags/hugo-partial%29
    /Page%28/categories/_index.md%29
    /Page%28/technology/cisco-vpn-save-password-macos/index.md%29
    /articles/2011/09/26/nstat-lookup-entry-failed-2
    /articles/2012/02/01/jekyll-directory-listing
    /articles/index.xml
    /page/3/
    /series/leadership/index.xml
    /atom.xml
    /articles/page/1/
    /Page%28/_index.md%29
    /Page%28/technology/fix-cisco-vpn-disconnections-mac-os-x-10.6.0-10.6.3/index.md%29
    /Page%28/tags/hugo-partial%29
    /Page%28/categories/_index.md%29
    /Page%28/technology/cisco-vpn-save-password-macos/index.md%29
    /tags/matlab
    /tags/matlab/
    /tags/non-existing
    /tags/non-existing/
    /categories/non-existing
    /categories/non-existing/
    /series/non-existing
    /series/non-existing/
    /de/tags/matlab
    /de/tags/matlab/
    /de/tags/non-existing
    /de/tags/non-existing/
    /de/categories/non-existing
    /de/categories/non-existing/
    /de/series/non-existing
    /de/series/non-existing/
)

for uri ($prior_urls); do
    get_uri $uri
done

