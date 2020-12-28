import datetime
import os
import pathlib
import shutil
import subprocess
import sys


def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def run_command(args, cwd=os.getcwd(), append_empty_line=True):
    try:
        print(f"Running {[str(arg) for arg in args] if len(args) <= 10 else args[0]} in {cwd}", flush=True)
        proc = subprocess.run(args, cwd=cwd)

        if append_empty_line:
            print(flush=True)

        return proc.returncode == 0
    except FileNotFoundError:
        return False


def ensure_command_availability(command, flag):
    if not run_command([command, flag]):
        fail(f"{command} is not available")


def ensure_repository_up_to_date(repo, repo_dir):
    if repo_dir.exists():
        if not run_command(["git", "pull"], cwd=repo_dir):
            fail(f"Could not pull {repo}")
    else:
        if not run_command(["git", "clone", "--depth", "1", f"https://github.com/{repo}.git", repo_dir]):
            fail(f"Could not clone {repo}")


def replace_in_file(path, target, replacement):
    with open(path, "r") as file:
        data = file.read()

    data = data.replace(target, replacement)

    with open(path, "w") as file:
        file.write(data)


def main():
    ensure_command_availability("git", "--version")
    ensure_command_availability("doxygen", "-v")
    ensure_command_availability("dot", "-V")

    project_root = pathlib.Path(os.getcwd())
    lean_dir = project_root / "Lean"

    ensure_repository_up_to_date("QuantConnect/Lean", lean_dir)

    if not run_command(["doxygen", "-w", "html", "_.html", "footer.html", "_.css"], cwd=lean_dir):
        fail("Doxygen failed while generating templates")

    replace_in_file(lean_dir / "footer.html", "$generatedby", 'API documentation for <a href="https://github.com/QuantConnect/Lean">QuantConnect/Lean</a> generated in <a href="https://github.com/jmerle/lean-api-docs">jmerle/lean-api-docs</a> by')
    replace_in_file(lean_dir / "footer.html", "<a ", '<a target="_blank" ')

    for file_name in ["Doxyfile", "MAIN_PAGE.md", "style.css"]:
        shutil.copyfile(project_root / file_name, lean_dir / file_name)

    timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    replace_in_file(lean_dir / "MAIN_PAGE.md", "$TIMESTAMP$", timestamp.replace("T", " ") + " UTC")

    if not run_command(["doxygen"], cwd=lean_dir):
        fail("Doxygen failed while generating documentation")

    print(f"API documentation is now available at file://{lean_dir}/_docs/index.html")


if __name__ == "__main__":
    main()
