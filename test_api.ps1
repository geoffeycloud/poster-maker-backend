# PowerShell script to test the AI Poster Maker API

# Test 1: Generate a Business Poster
Write-Host "Testing Business Poster Generation..." -ForegroundColor Green
$businessPoster = @{
    title = "Grand Opening Sale"
    description = "50% off everything in store!"
    theme = "corporate"
    size = "A4"
    background_prompt = "modern business storefront with elegant lighting"
    include_logo = $true
    additional_text = "Visit us at 123 Main Street | Call: (555) 123-4567"
} | ConvertTo-Json

$response1 = Invoke-RestMethod -Uri "http://localhost:8000/api/generate-poster" -Method Post -Body $businessPoster -ContentType "application/json"
Write-Host "Business Poster ID: $($response1.poster_id)" -ForegroundColor Yellow
Write-Host "Preview URL: http://localhost:8000$($response1.image_url)" -ForegroundColor Cyan

# Test 2: Generate a Social Media Post
Write-Host "`nTesting Social Media Post Generation..." -ForegroundColor Green
$socialPost = @{
    title = "Follow Your Dreams"
    description = "Motivational quote of the day"
    theme = "modern"
    size = "SOCIAL_MEDIA"
    background_prompt = "inspiring sunset over mountains"
    additional_text = "#motivation #dreams #success"
} | ConvertTo-Json

$response2 = Invoke-RestMethod -Uri "http://localhost:8000/api/generate-poster" -Method Post -Body $socialPost -ContentType "application/json"
Write-Host "Social Media Post ID: $($response2.poster_id)" -ForegroundColor Yellow
Write-Host "Preview URL: http://localhost:8000$($response2.image_url)" -ForegroundColor Cyan

# Test 3: Generate an Event Flyer
Write-Host "`nTesting Event Flyer Generation..." -ForegroundColor Green
$eventFlyer = @{
    title = "Tech Conference 2025"
    description = "The Future of AI and Innovation"
    theme = "professional"
    size = "LETTER"
    background_prompt = "futuristic tech conference hall with holographic displays"
    include_logo = $true
    additional_text = "December 15-16, 2025 | Register at techconf2025.com"
} | ConvertTo-Json

$response3 = Invoke-RestMethod -Uri "http://localhost:8000/api/generate-poster" -Method Post -Body $eventFlyer -ContentType "application/json"
Write-Host "Event Flyer ID: $($response3.poster_id)" -ForegroundColor Yellow
Write-Host "Preview URL: http://localhost:8000$($response3.image_url)" -ForegroundColor Cyan

# Test 4: Generate AI Text
Write-Host "`nTesting AI Text Generation..." -ForegroundColor Green
$textRequest = @{
    prompt = "Write a catchy tagline for a coffee shop"
    tone = "friendly"
    max_length = 100
} | ConvertTo-Json

$textResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/generate-text" -Method Post -Body $textRequest -ContentType "application/json"
Write-Host "Generated Text: $($textResponse.text)" -ForegroundColor Magenta

# Test 5: Get Available Templates
Write-Host "`nGetting Available Templates..." -ForegroundColor Green
$templates = Invoke-RestMethod -Uri "http://localhost:8000/api/templates" -Method Get
Write-Host "Available Templates:" -ForegroundColor Yellow
$templates.templates | ForEach-Object { Write-Host "  - $($_.name): $($_.description)" }

# Test 6: Get Available Themes
Write-Host "`nGetting Available Themes..." -ForegroundColor Green
$themes = Invoke-RestMethod -Uri "http://localhost:8000/api/themes" -Method Get
Write-Host "Available Themes:" -ForegroundColor Yellow
$themes.themes | ForEach-Object { Write-Host "  - $_" }

Write-Host "`nAll tests completed! Check the generated posters in the 'generated_posters' folder." -ForegroundColor Green
Write-Host "You can also view them in your browser using the preview URLs above." -ForegroundColor Green
