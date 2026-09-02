# Update all subpages:
# 1. Remove "Back to home" link (line 17 in nav)
# 2. Replace footer with single-line version

$files = @(
    'agents.html',
    'avatar-app.html', 
    'company-brain.html',
    'distribution.html',
    'future.html',
    'marketing.html',
    'mcp-server.html',
    'second-home-template.html',
    'smart.html',
    'virtual-mascot.html',
    'workflows.html'
)

# New single-line footer HTML
$newFooter = @'
    <footer class="page-footer" style="justify-content: center; text-align: center;">
      <div style="font-size: 12px; color: var(--ink-dim);">
        &copy; 2026 SlamDunk Technologies <span style="margin: 0 8px;">&middot;</span> 
        Powered by <a href="https://buddyfetch.ai" target="_blank" rel="noopener noreferrer" style="color: var(--ink); text-decoration: none;">BuddyFetch.AI</a> <span style="margin: 0 8px;">&middot;</span> 
        <a href="tel:+16196422087" style="color: var(--ink); text-decoration: underline; text-decoration-color: rgba(139,108,240,.55); text-underline-offset: 2px;">Call Buddy 619-642-2087</a> <span style="margin: 0 8px;">&middot;</span> 
        <a href="sms:+16196422087" style="color: var(--ink); text-decoration: underline; text-decoration-color: rgba(139,108,240,.55); text-underline-offset: 2px;">Text Buddy</a> <span style="margin: 0 8px;">&middot;</span> 
        CA DRE# 02162832 <span style="margin: 0 8px;">&middot;</span> NMLS# 2282987
      </div>
    </footer>
'@

foreach ($file in $files) {
    if (-not (Test-Path $file)) {
        Write-Host "Skipping $file (not found)"
        continue
    }
    
    $content = Get-Content $file -Raw
    
    # Remove "Back to home" link (usually on line 17)
    $content = $content -replace '<a class="back-link" href="index\.html">Back to home</a>\s*', ''
    
    # Replace footer section
    $content = $content -replace '(?s)<footer class="page-footer".*?</footer>', $newFooter
    
    Set-Content -Path $file -Value $content -NoNewline
    Write-Host "✅ Updated $file"
}

Write-Host "`nDone! Updated $($files.Count) files."
