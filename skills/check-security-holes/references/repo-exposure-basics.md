# Repo Exposure Basics

Use this reference when the request is about secrets in git, `.gitignore` gaps, mobile config files, or lightweight security gates before GitHub commit or release.

## Official anchors

- Git ignore rules apply only to untracked files. If a sensitive file is already tracked, adding it to `.gitignore` is not enough; the index entry still has to be removed. Sources:
  - https://git-scm.com/docs/gitignore
  - https://git-scm.com/docs/git-rm
- GitHub secret scanning and push protection detect supported secret formats and can stop pushes. Use alerts as evidence, not as proof that everything else is safe. Sources:
  - https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning
  - https://docs.github.com/en/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/protecting-pushes-with-secret-scanning
- Firebase Apple and Android config files are client configuration files with unique but non-secret identifiers. Firebase API keys are generally safe to include in code, but they still deserve API restrictions and App Check where relevant. Sources:
  - https://firebase.google.com/docs/ios/setup
  - https://firebase.google.com/docs/projects/api-keys
- Google Cloud service account keys are sensitive credentials. Prefer avoiding long-lived keys, and do not store them in source control. Source:
  - https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys

## Baseline checks for `repo-exposure-review`

1. Check the diff first.
   Look for newly added keys, `.env` files, signing material, certificates, service-account JSON, or mobile config files that were not part of the intended surface.

2. Check repository mechanics, not just content.
   If a file should stay local-only, verify both `.gitignore` and tracked status. A missing ignore rule and an already tracked file are different problems.

3. Classify vendor config files before escalating.
   `GoogleService-Info.plist` and `google-services.json` are not automatic secret leaks. Treat them as review items unless they contain extra secrets, violate explicit repo policy, or point to the wrong environment.

4. Escalate server credentials aggressively.
   Service-account JSON, PEM/P12/P8 private keys, JKS/keystore signing files, production `.env` files, OAuth client secrets, CI tokens, and long-lived bearer tokens should default to high severity.

5. Prefer actionable gate outcomes.
   The point of this mode is to decide whether a commit or release should be blocked, not to generate a long security roadmap.

## Practical severity rules

- `high`: real credential material, private keys, service-account keys, production env files, or tokens with clear abuse potential.
- `medium`: local-only config committed by mistake, ignore drift, ambiguous mobile config exposure, or missing allowlist decisions that can leak later.
- `review-only`: expected public client config tracked intentionally, with documented justification and no extra secret material.

## Search patterns that usually pay off

Use fast repository scans before deeper inspection.

```bash
rg --files | rg '(^|/)(\\.env(\\..*)?|GoogleService-Info\\.plist|google-services\\.json|.*(service-account|firebase-adminsdk).+\\.json|.*\\.(pem|p12|p8|key|jks|keystore|mobileprovision))$'
rg -n 'AIza[0-9A-Za-z\\-_]{20,}|BEGIN (RSA |EC |OPENSSH |)?PRIVATE KEY|client_secret|service_account|firebase-adminsdk|x-api-key|authorization: bearer' -S .
git ls-files | rg '(GoogleService-Info\\.plist|google-services\\.json|\\.env|\\.pem|\\.p8|service-account|firebase-adminsdk)'
```

## Decision shortcuts

- If the file is build-required mobile client config and official docs describe it as non-secret, do not auto-block. Record an allowlist decision and check environment separation.
- If the file contains private key material or server credentials, block the commit or release by default.
- If the problem is only `.gitignore` drift, note whether the file is already tracked. If it is tracked, the remediation must include removing it from the index, not just editing `.gitignore`.
