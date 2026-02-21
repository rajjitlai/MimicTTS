# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 1.0.x | Yes |

---

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability, please report it privately by contacting **[Rajjit Laishram](https://rajjitlaishram.netlify.app)** directly via the website.

Please include the following in your report:

- A clear description of the vulnerability
- Steps to reproduce the issue
- The potential impact
- Any suggested fixes, if available

You will receive a response within 7 days. If the issue is confirmed, a patch will be released as soon as possible.

---

## Scope

This project processes local audio files and runs a local TTS model. It does not transmit user audio or text to any external service (except for model downloads from HuggingFace). Ensure your `HF_TOKEN` is kept private and never committed to version control.

MimicTTS is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
