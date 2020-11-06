
local BOX_SIZE = 1

local eventFrame = CreateFrame("frame", "EventFrame")
eventFrame:RegisterEvent("PLAYER_ENTERING_WORLD")

local function initTexture(f)
    local t = f:CreateTexture(nil,"BACKGROUND")
    t:SetColorTexture(1, 1, 1, 1)
    t:SetAllPoints(f)
    return t
end

local function createFrame()
    local f = CreateFrame("Frame",nil,UIParent)
    f:SetFrameStrata("BACKGROUND")
    f:SetWidth(BOX_SIZE)
    f:SetHeight(BOX_SIZE)
    return f
end

local modeFrame = createFrame()
modeFrame:SetPoint("TOPLEFT", 0, 0)
local modeTexture = initTexture(modeFrame)
modeFrame:Show()

local statsFrame = createFrame()
statsFrame:SetPoint("BOTTOMLEFT", 0, 0)
local statsTexture = initTexture(statsFrame)
statsFrame:Show()

local function updateComboPoints()
    local points = GetComboPoints("player", "target") -- UnitPower for combo points does not work in Classic.
    statsTexture:SetColorTexture(points / 255, points / 255, points / 255, 1)
end

local function updateHealth()
    local hp_fraction = UnitHealth("player") / UnitHealthMax("player")
    statsTexture:SetColorTexture(hp_fraction, hp_fraction, hp_fraction, 1)
end

local function updateEnergy()
    local max_energy = UnitPowerMax("player", 3) -- Constant seems to have an off-by-one error.
    if max_energy == 0 then
        statsTexture:SetColorTexture(0, 0, 0, 1)
        return 
    end
    local energy_fraction = UnitPower("player", 3) / max_energy 
    statsTexture:SetColorTexture(energy_fraction, energy_fraction, energy_fraction, 1)
end

local function updateRage()
    local max_rage = UnitPowerMax("player", 1) -- Constant seems to have an off-by-one error.
    if max_rage == 0 then
        statsTexture:SetColorTexture(0, 0, 0, 1)
        return
    end

    local rage_fraction = UnitPower("player", 1) / max_rage 
    statsTexture:SetColorTexture(rage_fraction, rage_fraction, rage_fraction, 1)
end

local function updateCombat()
    local pixel_value
    if UnitAffectingCombat("player") then 
        pixel_value = 1 / 255.0
    else
        pixel_value = 0
    end
    statsTexture:SetColorTexture(pixel_value, pixel_value, pixel_value, 1)
end

local function updateModeTexture(pixel_val)
    modeTexture:SetColorTexture(pixel_val / 255.0, pixel_val / 255.0, pixel_val / 255.0, 1)
end

local function shouldTriggerHpUpdate(event, ...)
    if event ~= "UNIT_HEALTH" then
        return false
    end
    local unit_id = ...
    return unit_id == "player"
end

local function isUnitPowerFrequentEventForPlayer(target_power_type, event, ...)
    if (event ~= "UNIT_POWER_FREQUENT") then
        return false
    end
    local unit_id, power_type = ...
    return unit_id == "player" and power_type == target_power_type
end

local function shouldTriggerComboPointsUpdate(event, ...)
    return isUnitPowerFrequentEventForPlayer("COMBO_POINTS", event, ...)
end

local function shouldTriggerEnergyUpdate(event, ...)
    return isUnitPowerFrequentEventForPlayer("ENERGY", event, ...)
end

local function shouldTriggerRageUpdate(event, ...)
    return isUnitPowerFrequentEventForPlayer("RAGE", event, ...)
end

local function shouldTriggerCombatUpdate(event, ...)
    local is_regen_event =  event == "PLAYER_REGEN_ENABLED" or event == "PLAYER_REGEN_DISABLED"
    return is_regen_event
end

-- The mode encodes the pixel value of the mode texture.
-- This must match the values in the Python script.
Modes = {
    HP = 0,
    COMBO_POINTS = 1,
    ENERGY = 2,
    RAGE = 3,
    COMBAT = 4
}

local mode = Modes.HP

-- (1) Plugins for whether an event should trigger an update
event_should_trigger_update_plugins = {
    [Modes.HP] = shouldTriggerHpUpdate,
    [Modes.COMBO_POINTS] = shouldTriggerComboPointsUpdate,
    [Modes.ENERGY] = shouldTriggerEnergyUpdate,
    [Modes.RAGE] = shouldTriggerRageUpdate,
    [Modes.COMBAT] = shouldTriggerCombatUpdate
}

-- (2) Plugins for the update itself
update_plugins = {
    [Modes.HP] = updateHealth,
    [Modes.COMBO_POINTS] = updateComboPoints,
    [Modes.ENERGY] = updateEnergy,
    [Modes.RAGE] = updateRage,
    [Modes.COMBAT] = updateCombat
}

-- (3) Name plugins for mode values.
name_plugins = {
    [Modes.HP] = "HP",
    [Modes.COMBO_POINTS] = "Combo Points",
    [Modes.ENERGY] = "Energy",
    [Modes.RAGE] = "Rage",
    [Modes.COMBAT] = "Combat"
}

-- (4) Register the events for each mode.
event_plugins = {
    [Modes.HP] = {"UNIT_HEALTH"},
    [Modes.COMBO_POINTS] = {"UNIT_POWER_FREQUENT"},
    [Modes.ENERGY] = {"UNIT_POWER_FREQUENT"},
    [Modes.RAGE] = {"UNIT_POWER_FREQUENT"},
    [Modes.COMBAT] = {"PLAYER_REGEN_ENABLED", "PLAYER_REGEN_DISABLED"}
}

for _, event_list in pairs(event_plugins) do
    for _, event in pairs(event_list) do
        eventFrame:RegisterEvent(event)
    end
end

local function SetModeCallback(msg, editbox)
    local msg_mode = tonumber(msg)
    local plugin = update_plugins[msg_mode]
    if plugin == nil then
        print(string.format('Mode %s not recognized.', msg))
        return
    end

    mode = msg_mode
    print(string.format('Setting mode to %s.', name_plugins[msg_mode]))
    updateModeTexture(mode)
    plugin()
  end
  
SLASH_SETMODE1 = '/setmode'
SlashCmdList["SETMODE"] = SetModeCallback

EventFrame:SetScript("OnEvent", function(self, event, ...)
    if event_should_trigger_update_plugins[mode](event, ...) then
        update_plugins[mode]()
        return
    end
    if (event == "PLAYER_ENTERING_WORLD") then
        update_plugins[mode]()
        updateModeTexture(mode)
        return
    end
end)