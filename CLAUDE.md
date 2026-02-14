# CLAUDE.md - AI Assistant Guide for apat

## Project Overview

**apat** (a path) is a personalized information aggregator tool written in Go. It runs an HTTP server on port 8080 that fetches and displays content from RSS/Atom feeds and web-scraped "hot topics," organized by user-configured topic categories.

## Repository Structure

```
apat/
├── apat.go              # Single-file Go application (main source)
├── README.md            # Project documentation
├── LICENSE              # GPLv3
├── CLAUDE.md            # This file
├── topics/              # Topic marker files (empty files, names define categories)
│   ├── baseball
│   ├── cloud
│   ├── databases
│   ├── devops
│   ├── golang
│   ├── lapresse
│   ├── linux
│   ├── news
│   ├── ovh
│   └── security
├── sources/             # Feed URL lists and scraping configs
│   ├── hot-topics.src   # Web scraping targets (format: URL - Name - Label - Regex)
│   ├── security.src     # One RSS/Atom feed URL per line
│   ├── devops.src
│   ├── cloud.src
│   ├── news.src
│   ├── linux.src
│   ├── lapresse.src
│   ├── databases.src
│   ├── golang.src
│   ├── baseball.src
│   ├── soccer.src
│   └── ovh.src
├── hot-topics.src.bkp   # Config backups (not tracked actively)
├── hot-topics.src.bkp2
└── security.src.bkp
```

## Architecture

The application is a single-file Go program (`apat.go`) with two functions:

- **`main()`** - Registers the HTTP handler and starts the server on `:8080`.
- **`handler(w, r)`** - Handles every HTTP request by:
  1. Rendering an HTML page with a timestamp header.
  2. Reading `sources/hot-topics.src` and scraping each URL with a regex to extract a status value.
  3. Reading the `topics/` directory to discover all topic categories.
  4. For each topic, reading `sources/<topic>.src` and parsing each RSS/Atom feed URL via the `gofeed` library, displaying the 3 most recent items per feed.

### Configuration System

- **Adding a topic:** Create an empty file in `topics/` with the topic name, and a corresponding `sources/<topic-name>.src` file with one RSS/Atom feed URL per line.
- **Hot topics format:** Each line in `sources/hot-topics.src` follows `URL - DisplayName - Label - RegexPattern` (space-dash-space delimited).
- **Feed sources format:** Each line in `sources/*.src` (except hot-topics) is a plain RSS/Atom feed URL.

## Technology Stack

- **Language:** Go
- **External dependency:** `github.com/mmcdole/gofeed` (RSS/Atom feed parser)
- **No go.mod/go.sum:** This is a legacy pre-Go-modules project. Dependencies are managed via `GOPATH`.

## Build and Run

```bash
# Run directly
go run apat.go

# Compile and run
go build -o apat apat.go
./apat

# The server listens on http://localhost:8080
```

There is no Makefile, build script, or task runner configured.

## Testing

No tests exist in this project. There is no testing framework or test configuration.

When adding tests, use Go's standard `testing` package and name test files with the `_test.go` suffix (e.g., `apat_test.go`).

## Linting and Formatting

No linting or formatting tools are configured. Standard Go tools apply:

```bash
gofmt -w apat.go      # Format code
go vet ./...           # Static analysis
```

## CI/CD

No CI/CD pipeline is configured. There are no GitHub Actions workflows or other automation.

## Code Conventions

- Single-file architecture; all application logic resides in `apat.go`.
- HTML is generated inline via `fmt.Fprintf` calls writing directly to the `http.ResponseWriter`.
- Configuration is file-based (plain text files in `topics/` and `sources/`).
- Error handling is minimal; some errors are silently ignored (e.g., `os.Open` failures).
- The `defer resp.Body.Close()` calls inside loops are a known issue (deferred calls accumulate until function return).

## Known Technical Debt

- Uses deprecated `io/ioutil` package (replaced by `io` and `os` in Go 1.16+).
- No `go.mod` file; should be initialized with `go mod init` for modern Go tooling.
- `defer` inside loops in the `handler` function delays resource cleanup until the handler returns.
- No input validation or error handling for missing source files.
- No caching; feeds are fetched on every HTTP request.
- Hardcoded port (`:8080`) with no configuration option.
- Nil check on `feed.Items[i]` at line 109 dereferences the nil pointer on the next lines (bug).

## Making Changes

### Adding a new topic
1. Create an empty file: `touch topics/<topic-name>`
2. Create a source file: `echo "https://example.com/feed.xml" > sources/<topic-name>.src`
3. Add one RSS/Atom feed URL per line to the source file.

### Adding a hot topic
Add a line to `sources/hot-topics.src` in the format:
```
https://example.com/page - DisplayName - Label - RegexPattern
```
The regex should have one capture group whose match will be displayed.

### Modifying application code
All logic is in `apat.go`. After changes, verify with:
```bash
go build apat.go
go vet ./...
```
