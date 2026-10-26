# Attribution and repository privacy

Official project attribution uses **S. Poole**. Elsewhere, use neutral roles such
as “the author”, “the project owner” or “User”. Do not add personal names,
contact addresses, account handles or workstation-specific home paths.
Third-party scientific authors retain their proper names and citations.

On 26 October 2026 the project owner authorized sanitizing the repository and
its archives. This supersedes the earlier instruction to preserve identifying
source bytes. Scientific data and arguments are retained; personal source URLs,
identifiers, editor metadata and authorship metadata are sanitized. Current
integrity manifests refer to the sanitized representations. They no longer
certify identity with the original, identifying exports.

Source IDs use stable opaque local aliases. `source://` and `repository://`
references identify removed external source locations; they are not replacement
live websites. Local source inventories and archived scientific contents remain
available. Research results do not become new experiments merely because their
packaging and identifying metadata changed.

Local identity policies and recovery copies belong only in ignored `.local/`
storage. Do not commit an identity map, original export or original Git bundle.
Once this privacy migration is complete, preserve the sanitized evidence bytes
unless another explicit migration is authorized.

Use `scripts/check_anonymity.py` for generic publication checks. A private local
policy adds checks for known identifiers without putting them in the repository.
The check covers nested ZIP/Word files and PDF text/metadata; it cannot certify
anonymity against inference from research content or outside copies.

The owner explicitly chose to retain the current GitHub address. That address
still reveals the hosting account. Sanitizing history does not erase third-party
clones, forks, cached pages or records of earlier publication. The scope is
sanitized contents and attribution, not a promise of unlinkable authorship.
