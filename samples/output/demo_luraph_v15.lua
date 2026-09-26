-- Deobfuscated by ccjvwsod on Discord
-- Detected obfuscation: Luraph v15
-- behaviour trace of demo_luraph_v15.lua
-- run status: finished
-- 13 statements recorded in 0.01s

--@1
local Players = game:GetService("Players")
--@1
local ScreenGui = Instance.new("ScreenGui")
--@1
ScreenGui.Name = "LPHPanel_Luraph"
--@1
local PlayerGui = Players.LocalPlayer:WaitForChild("PlayerGui")
--@1
ScreenGui.Parent = PlayerGui
--@1
local TextLabel = Instance.new("TextLabel")
--@1
TextLabel.Size = UDim2.new(0, 220, 0, 40)
--@1
TextLabel.Text = "cargando 6"
--@1
TextLabel.Parent = ScreenGui
--@1
task.wait(0.2)
--@1
print("[demo]", "cargando 6", "LPHPanel_Luraph")
--@1
TextLabel.Text = "listo"
--@1
getgenv().LPH_DEMO = true
