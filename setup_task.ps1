$trigger = New-ScheduledTaskTrigger -Daily -At "08:05"
$action = New-ScheduledTaskAction -Execute "C:\Users\Lenovo\Desktop\更新APEC动态.bat"
Register-ScheduledTask -TaskName "APEC动态追踪" -Trigger $trigger -Action $action -Description "每天早上8:05更新APEC动态看板" -Force
Write-Host "定时任务已创建"
