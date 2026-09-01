$url = 'https://slamdunktechnologies.com/agents'
$html = (Invoke-WebRequest -Uri $url -UseBasicParsing -MaximumRedirection 5).Content
if ($html -match 'bullet-nav') { Write-Output 'bullet-nav FOUND' } else { Write-Output 'bullet-nav MISSING' }
if ($html -match 'href="agents.html" class="active"') { Write-Output 'agents marked ACTIVE' }
foreach ($p in @('workflows','marketing','smart','future')) {
  $pat = 'href="' + $p + '.html"'
  if ($html -match [regex]::Escape($pat)) { Write-Output ($p + ' link present') }
}