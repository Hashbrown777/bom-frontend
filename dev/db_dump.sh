#!/bin/bash

`pg_dump bom -U bom -W | gzip -c | cat > bom_$(date +%Y-%m-%d-%H.%M.%S).sql.gz`

