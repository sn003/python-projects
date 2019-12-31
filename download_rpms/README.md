This script downloads all of the rpms configured in the pkglist.conf.

Artifactory where all of the rpms are stored remotely.

Usage: python3 download_rpms.py <artifacory_url> <pkglist.conf>

This script uses concurrent.futures.ThreadPoolExecutor functionality to paralley download all of the configured rpms simultaneously.

Note: Earlier rpms were downloaded serially, approximately it took 3 mins to download 200rpms.
      With ThreadPoolExecutor, it takes only ~20Secs. 

