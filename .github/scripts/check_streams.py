name: Validate Stream URLs
on: [push, schedule]

jobs:
  check-urls:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install dependencies
        run: pip install requests m3u8
      - name: Check stream availability
        run: |
          python .github/scripts/check_streams.py