## HUD — Game UI overlay
extends CanvasLayer

var grid_map: Node2D
var main_node: Node2D
var selected_tower_type: String = ""

var gold_label: Label
var lives_label: Label
var wave_label: Label
var status_label: Label
var next_wave_btn: Button

func _ready() -> void:
	GameManager.gold_changed.connect(_on_gold_changed)
	GameManager.lives_changed.connect(_on_lives_changed)
	GameManager.wave_changed.connect(_on_wave_changed)
	GameManager.game_over.connect(_on_game_over)
	GameManager.wave_started.connect(_on_wave_started)
	GameManager.wave_completed.connect(_on_wave_completed)
	
	_build_ui()

func _build_ui() -> void:
	# === TOP BAR ===
	var top_bar := PanelContainer.new()
	top_bar.set_anchors_preset(Control.PRESET_TOP_WIDE)
	top_bar.offset_bottom = 44
	
	# Dark background
	var top_style := StyleBoxFlat.new()
	top_style.bg_color = Color(0.08, 0.06, 0.04, 0.92)
	top_bar.add_theme_stylebox_override("panel", top_style)
	add_child(top_bar)
	
	var top_hbox := HBoxContainer.new()
	top_hbox.set_anchors_preset(Control.PRESET_TOP_WIDE)
	top_hbox.offset_top = 8
	top_hbox.offset_bottom = 40
	top_hbox.offset_left = 12
	top_hbox.offset_right = -12
	top_hbox.add_theme_constant_override("separation", 20)
	add_child(top_hbox)
	
	gold_label = _make_label("Gold: 100", 20, Color(1.0, 0.85, 0.2))
	top_hbox.add_child(gold_label)
	
	lives_label = _make_label("Lives: 20", 20, Color(1.0, 0.35, 0.35))
	top_hbox.add_child(lives_label)
	
	wave_label = _make_label("Wave: 0/5", 20, Color(0.7, 0.85, 1.0))
	top_hbox.add_child(wave_label)
	
	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	top_hbox.add_child(spacer)
	
	status_label = _make_label("BUILD PHASE", 20, Color(0.4, 1.0, 0.4))
	top_hbox.add_child(status_label)
	
	# === BOTTOM BAR ===
	var bottom_bar := PanelContainer.new()
	bottom_bar.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	bottom_bar.offset_top = -56
	var bot_style := StyleBoxFlat.new()
	bot_style.bg_color = Color(0.08, 0.06, 0.04, 0.92)
	bottom_bar.add_theme_stylebox_override("panel", bot_style)
	add_child(bottom_bar)
	
	var bot_hbox := HBoxContainer.new()
	bot_hbox.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	bot_hbox.offset_top = -52
	bot_hbox.offset_bottom = -6
	bot_hbox.offset_left = 12
	bot_hbox.offset_right = -12
	bot_hbox.add_theme_constant_override("separation", 12)
	add_child(bot_hbox)
	
	# Tower buttons
	for tower_info: Dictionary in [
		{"name": "Archer", "type": "archer", "cost": 50},
		{"name": "Catapult", "type": "catapult", "cost": 100},
		{"name": "Wall", "type": "wall", "cost": 25},
	]:
		var btn := Button.new()
		btn.text = "%s (%dg)" % [tower_info.name, tower_info.cost]
		btn.custom_minimum_size = Vector2(130, 38)
		btn.tooltip_text = "Place %s tower" % tower_info.name
		var ttype: String = tower_info.type
		btn.pressed.connect(_on_tower_btn.bind(ttype))
		bot_hbox.add_child(btn)
	
	var spacer2 := Control.new()
	spacer2.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	bot_hbox.add_child(spacer2)
	
	next_wave_btn = Button.new()
	next_wave_btn.text = "▶ Start Wave"
	next_wave_btn.custom_minimum_size = Vector2(160, 38)
	next_wave_btn.pressed.connect(_on_next_wave)
	bot_hbox.add_child(next_wave_btn)

func _make_label(text: String, size: int, color: Color) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", color)
	l.custom_minimum_size = Vector2(110, 28)
	return l

func _input(event: InputEvent) -> void:
	if not (event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT):
		return
	if selected_tower_type == "":
		return
	if not grid_map:
		return
	
	# Get Main node reference
	if not main_node:
		main_node = grid_map.get_parent() as Node2D
	if not main_node:
		return
	
	# Convert screen click to world position via camera
	var camera := get_viewport().get_camera_2d()
	var world_pos: Vector2
	if camera:
		world_pos = (event.position - get_viewport().get_visible_rect().size * 0.5) * camera.zoom + camera.global_position
	else:
		world_pos = event.position
	
	var gpos: Vector2i = grid_map.world_to_grid(world_pos)
	
	if main_node.has_method("place_tower_at"):
		if main_node.place_tower_at(gpos, selected_tower_type):
			status_label.text = "Placed %s!" % selected_tower_type.capitalize()
		else:
			status_label.text = "Can't place there!"

func _on_tower_btn(type: String) -> void:
	if selected_tower_type == type:
		selected_tower_type = ""
		status_label.text = "BUILD PHASE"
		status_label.add_theme_color_override("font_color", Color(0.4, 1.0, 0.4))
		return
	if not GameManager.can_afford(type):
		status_label.text = "Not enough gold!"
		status_label.add_theme_color_override("font_color", Color(1.0, 0.3, 0.3))
		return
	selected_tower_type = type
	status_label.text = "Click map to place: " + type.to_upper()
	status_label.add_theme_color_override("font_color", Color(1.0, 0.85, 0.2))

func _on_next_wave() -> void:
	if not GameManager.is_build_phase:
		return
	selected_tower_type = ""
	GameManager.start_wave()
	next_wave_btn.disabled = true
	next_wave_btn.text = "Wave in progress..."

func _on_gold_changed(amount: int) -> void:
	gold_label.text = "Gold: %d" % amount

func _on_lives_changed(amount: int) -> void:
	lives_label.text = "Lives: %d" % amount

func _on_wave_changed(wave: int, total: int) -> void:
	wave_label.text = "Wave: %d/%d" % [wave, total]

func _on_game_over(won: bool) -> void:
	if won:
		status_label.text = "VICTORY!"
		status_label.add_theme_color_override("font_color", Color(0.2, 1.0, 0.2))
		next_wave_btn.text = "Level Complete!"
	else:
		status_label.text = "DEFEAT"
		status_label.add_theme_color_override("font_color", Color(1.0, 0.2, 0.2))
		next_wave_btn.text = "Game Over"
	next_wave_btn.disabled = true

func _on_wave_started(wave: int) -> void:
	status_label.text = "WAVE %d — Fight!" % wave
	status_label.add_theme_color_override("font_color", Color(1.0, 0.4, 0.3))

func _on_wave_completed(wave: int) -> void:
	status_label.text = "BUILD PHASE"
	status_label.add_theme_color_override("font_color", Color(0.4, 1.0, 0.4))
	next_wave_btn.disabled = false
	next_wave_btn.text = "▶ Next Wave"
