param(
  [Parameter(Mandatory = $true)]
  [string]$GithubUser,

  [Parameter(Mandatory = $true)]
  [string]$RepoName
)

$root = Resolve-Path "$PSScriptRoot\.."
$files = @(
  "$root\platform\helm\resume-ai\values.yaml",
  "$root\platform\gitops\argocd\resume-ai-staging.yaml",
  "$root\platform\gitops\argocd\resume-ai-prod.yaml"
)

foreach ($file in $files) {
  $content = Get-Content -LiteralPath $file -Raw
  $content = $content.Replace("YOUR_GITHUB_USERNAME", $GithubUser)
  $content = $content.Replace("YOUR_REPO", $RepoName)
  Set-Content -LiteralPath $file -Value $content -NoNewline
}

Write-Host "Updated GitOps placeholders for $GithubUser/$RepoName"

