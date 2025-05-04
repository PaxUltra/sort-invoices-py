# TODO

## Features to Add

### Verbose mode

`parser.add_argument("--verbose", action="store_true", help="Show detailed logging output in the terminal.")`

### Overwrite handling

>You might want to add logic to prevent overwriting files in the destination (and maybe in the archive), or at least log a warning. A --overwrite flag could let the user explicitly opt-in.

### Summary Report

> Print or log a summary at the end:
>
> - Total files found
> - Total successfully processed
> - Files skipped (and why)
> - Archive path (if used)

> This could be particularly useful in automated or batch runs."

### Configuration File Support

> For repeat runs, it might be helpful to support loading defaults from a config file (e.g., sort_invoices.toml or .ini)—optional, but useful for power users or batch automation.

### Testing Flags

> When you update your tests, you might add a --test-mode or --no-logfile flag that simplifies or disables logging during test runs, especially useful in CI environments.