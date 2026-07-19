# Zenodo DOI (one-time, ~5 minutes)

A **Zenodo DOI** is the standard FAIR citation identifier for GitHub releases.
GitHub cannot mint that DOI until Zenodo is linked once. Deposit metadata for
uploads lives in [.zenodo.json](../.zenodo.json).

## Steps

1. Sign in at [zenodo.org](https://zenodo.org) with **GitHub** (account that can access **Fratres-X-AI**).
2. Open [Zenodo GitHub settings](https://zenodo.org/account/settings/github/).
3. Flip **mavmrf** to **On**.
4. On GitHub, create a new release (for example 0.2.1), or use Zenodo's
   "Send to Zenodo" on an existing release if offered.
5. Copy the DOI from the Zenodo deposit page.
6. Update [CITATION.cff](../CITATION.cff):

`yaml
doi: 10.5281/zenodo.XXXXXXXX
identifiers:
  - type: doi
    value: 10.5281/zenodo.XXXXXXXX
`

## Until the DOI exists

Cite via GitHub + CITATION.cff. Browse Software Heritage origin:

https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/Fratres-X-AI/mavmrf
