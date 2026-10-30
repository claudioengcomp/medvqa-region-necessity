#!/usr/bin/env bash
# HEAL-test batch from the workstation to gpu-server-a with checksum (rsync -c verifies files that already exist; new transfers are checked by rsync itself), then sha256sum -c at the destination.
cd "$HOME/Documents/doutorado/data_drive_sync.nosync/raw/vindr-cxr/1.0.0"
D=${LAB_ROOT}/doutorado/data/raw/vindr-cxr/1.0.0
echo "rsync inicio $(date -u +%FT%TZ)"
rsync -a -c --files-from=ids_heal_test.txt --stats . gpu-server-a:$D/ 2>&1 | tail -15
scp -q sha256_heal_test.txt gpu-server-a:$D/sha256_heal_test.txt
echo "sha256 no gpu1 $(date -u +%FT%TZ)"
ssh gpu-server-a "cd $D && sha256sum -c sha256_heal_test.txt 2>/dev/null | grep -c ': OK$'; sha256sum -c sha256_heal_test.txt 2>/dev/null | grep -vc ': OK$'; du -sh train | cut -f1"
echo "RSYNC_DONE $(date -u +%FT%TZ)"
