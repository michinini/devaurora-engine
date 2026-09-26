-- Protected by Luraph v15 - https://lura.ph
-- LPH_JIT(true) LPH_ENCSTR LPH_PRECHECK LPH_ENCBUF
local IlllIlIIlllIlIlI = "\76\117\114\97\112\104"
local v0 = game:GetService("Players")
local v1 = Instance.new("ScreenGui")
v1.Name = "LPHPanel_" .. IlllIlIIlllIlIlI
v1.Parent = v0.LocalPlayer:WaitForChild("PlayerGui")
local v2 = Instance.new("TextLabel")
v2.Size = UDim2.new(0, 220, 0, 40)
v2.Text = "cargando " .. tostring(#IlllIlIIlllIlIlI)
v2.Parent = v1
task.wait(0.2)
print("[demo]", v2.Text, v1.Name)
v2.Text = "listo"
getgenv().LPH_DEMO = true
