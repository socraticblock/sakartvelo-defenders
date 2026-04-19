## Enemy — Base enemy that moves along the path
extends CharacterBody2D

signal reached_end
signal died

@export var max_health: float = 50.0
@export var move_speed: float = 80.0
@export var reward: int = 10
@export var damage_to_player: int = 1

var health: float = 50.0
var path: Array = []
var path_index: int = 0
var alive: bool = true
var sprite: Sprite2D
var health_bar: ProgressBar

func _ready() -> void:
	health = max_health
	_create_visuals()
	add_to_group("enemies")

func _create_visuals() -> void:
	# Try loading cel-shaded sprite
	sprite = Sprite2D.new()
	var tex: Texture2D = _get_sprite()
	if tex:
		sprite.texture = tex
		sprite.scale = Vector2(1.5, 1.5)
	else:
		# Fallback: programmatic warrior shape
		var img := Image.create(32, 44, false, Image.FORMAT_RGBA8)
		img.fill(Color(0, 0, 0, 0))
		# Body
		for y in range(12, 36):
			for x in range(10, 22):
				img.set_pixel(x, y, Color(0.10, 0.22, 0.15))  # Fur
		# Head
		for y in range(2, 14):
			for x in range(11, 21):
				if (x - 16) * (x - 16) + (y - 8) * (y - 8) < 36:
					img.set_pixel(x, y, Color(0.82, 0.69, 0.56))  # Skin
		# Club
		for y in range(8, 30):
			img.set_pixel(22, y, Color(0.54, 0.45, 0.33))
		# Shield
		for y in range(18, 30):
			for x in range(4, 10):
				img.set_pixel(x, y, Color(0.45, 0.35, 0.22))
		var tex2 := ImageTexture.create_from_image(img)
		sprite.texture = tex2
	sprite.centered = true
	add_child(sprite)
	
	# Health bar
	health_bar = ProgressBar.new()
	health_bar.min_value = 0.0
	health_bar.max_value = max_health
	health_bar.value = max_health
	health_bar.custom_minimum_size = Vector2(30, 4)
	health_bar.position = Vector2(-15, -35)
	health_bar.show_percentage = false
	var bg_style := StyleBoxFlat.new()
	bg_style.bg_color = Color(0.15, 0.15, 0.15, 0.8)
	bg_style.corner_radius_top_left = 2
	bg_style.corner_radius_bottom_left = 2
	bg_style.corner_radius_top_right = 2
	bg_style.corner_radius_bottom_right = 2
	health_bar.add_theme_stylebox_override("background", bg_style)
	var fill_style := StyleBoxFlat.new()
	fill_style.bg_color = Color(0.85, 0.2, 0.2)
	fill_style.corner_radius_top_left = 2
	fill_style.corner_radius_bottom_left = 2
	fill_style.corner_radius_top_right = 2
	fill_style.corner_radius_bottom_right = 2
	health_bar.add_theme_stylebox_override("fill", fill_style)
	add_child(health_bar)

func _get_sprite() -> Texture2D:
	var p := "res://assets/sprites/enemies/enemy_e00_primitive_warrior_v5_cel.png"
	if ResourceLoader.exists(p):
		return load(p)
	return null

func set_path(new_path: Array) -> void:
	path = new_path
	path_index = 0
	if path.size() > 0:
		global_position = path[0]

func _physics_process(_delta: float) -> void:
	if not alive or path.is_empty():
		return
	
	if path_index >= path.size():
		_reach_end()
		return
	
	var target: Vector2 = path[path_index]
	var to_target: Vector2 = target - global_position
	
	if to_target.length() < 5.0:
		path_index += 1
		return
	
	var direction: Vector2 = to_target.normalized()
	velocity = direction * move_speed
	move_and_slide()
	
	if sprite:
		if velocity.x < -5.0:
			sprite.flip_h = true
		elif velocity.x > 5.0:
			sprite.flip_h = false

func take_damage(amount: float) -> void:
	if not alive:
		return
	health -= amount
	if health_bar:
		health_bar.value = health
	if sprite:
		sprite.modulate = Color(2.0, 0.5, 0.5)
		var tween := create_tween()
		tween.tween_property(sprite, "modulate", Color.WHITE, 0.12)
	if health <= 0.0:
		_die()

func _die() -> void:
	alive = false
	died.emit()
	GameManager.enemy_killed(reward)
	queue_free()

func _reach_end() -> void:
	alive = false
	reached_end.emit()
	GameManager.enemy_reached_end()
	queue_free()
