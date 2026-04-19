## Tower — Base tower with targeting and projectile shooting
extends Node2D

@export var tower_type: String = "archer"
@export var damage: float = 15.0
@export var attack_range: float = 150.0
@export var attack_speed: float = 1.0
@export var projectile_speed: float = 300.0
@export var level: int = 1

var attack_timer: float = 0.0
var target: CharacterBody2D = null
var grid_pos: Vector2i = Vector2i(-1, -1)
var sprite: Sprite2D
var range_visual: Node2D
var can_shoot: bool = true

func _ready() -> void:
	can_shoot = tower_type != "wall"
	_create_visuals()

func _create_visuals() -> void:
	sprite = Sprite2D.new()
	var tex: Texture2D = _get_sprite()
	if tex:
		sprite.texture = tex
	else:
		# Programmatic tower shape
		var size_x := 48 if tower_type == "catapult" else 36 if tower_type == "wall" else 32
		var size_y := 48 if tower_type == "wall" else 56
		var img := Image.create(size_x, size_y, false, Image.FORMAT_RGBA8)
		img.fill(Color(0, 0, 0, 0))
		
		if tower_type == "archer":
			# Stone base
			for y in range(24, 48):
				for x in range(4, 28):
					img.set_pixel(x, y, Color(0.54, 0.45, 0.33))
			# Tower body
			for y in range(10, 28):
				for x in range(6, 26):
					img.set_pixel(x, y, Color(0.45, 0.35, 0.22))
			# Pointed roof
			for y in range(0, 12):
				var w := int(10 * (12 - y) / 12)
				for x in range(16 - w, 16 + w):
					img.set_pixel(x, y, Color(0.10, 0.22, 0.15))
		elif tower_type == "catapult":
			# Wooden platform
			for y in range(20, 28):
				for x in range(2, 46):
					img.set_pixel(x, y, Color(0.45, 0.35, 0.22))
			# Arm
			for y in range(4, 22):
				img.set_pixel(24, y, Color(0.35, 0.27, 0.18))
			# Bucket
			for y in range(2, 8):
				for x in range(20, 29):
					img.set_pixel(x, y, Color(0.54, 0.45, 0.33))
			# Wheels
			for y in range(28, 36):
				for x in [8, 9, 38, 39]:
					img.set_pixel(x, y, Color(0.25, 0.25, 0.25))
		else:  # wall
			for y in range(0, 48):
				for x in range(0, 48):
					var is_battlement: bool = y < 12 and (x % 12 < 6)
					if y >= 12 or is_battlement:
						img.set_pixel(x, y, Color(0.54, 0.45, 0.33))
		
		var tex2 := ImageTexture.create_from_image(img)
		sprite.texture = tex2
	
	sprite.centered = true
	sprite.offset = Vector2(0, -20)  # Anchor bottom
	add_child(sprite)
	
	# Range circle
	range_visual = Node2D.new()
	range_visual.set_script(load("res://scripts/towers/range_indicator.gd"))
	range_visual.range_radius = attack_range
	range_visual.visible = false
	add_child(range_visual)

func _get_sprite() -> Texture2D:
	var p := "res://assets/sprites/towers/tower_archer_e00.png"
	if ResourceLoader.exists(p):
		return load(p)
	return null

func _process(delta: float) -> void:
	if not can_shoot:
		return
	attack_timer -= delta
	if attack_timer <= 0.0:
		_acquire_target()
		if target and is_instance_valid(target) and target.alive:
			_fire()
			attack_timer = 1.0 / attack_speed

func _acquire_target() -> void:
	target = null
	var best_dist: float = attack_range
	var enemies := get_tree().get_nodes_in_group("enemies")
	for e in enemies:
		var enemy := e as CharacterBody2D
		if not enemy or not enemy.alive:
			continue
		var dist: float = global_position.distance_to(enemy.global_position)
		if dist < best_dist:
			best_dist = dist
			target = enemy

func _fire() -> void:
	if not target:
		return
	var proj := CharacterBody2D.new()
	proj.set_script(load("res://scripts/projectiles/projectile.gd"))
	proj.global_position = global_position + Vector2(0, -20)
	proj.set("target", target)
	proj.set("damage", damage)
	proj.set("speed", projectile_speed)
	get_parent().add_child(proj)

func show_range() -> void:
	if range_visual:
		range_visual.visible = true

func hide_range() -> void:
	if range_visual:
		range_visual.visible = false

func upgrade() -> bool:
	if level >= 3:
		return false
	level += 1
	damage *= 1.4
	attack_range *= 1.1
	attack_speed *= 1.15
	if range_visual:
		range_visual.range_radius = attack_range
	return true
