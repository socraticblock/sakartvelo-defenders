## Projectile — Homing arrow/boulder toward target
extends CharacterBody2D

var target: CharacterBody2D
var damage: float = 15.0
var speed: float = 300.0
var lifetime: float = 3.0

func _ready() -> void:
	# Arrow visual
	var sprite := Sprite2D.new()
	var tex_path := "res://assets/sprites/projectiles/arrow_gold.png"
	if ResourceLoader.exists(tex_path):
		sprite.texture = load(tex_path)
	else:
		var img := Image.create(10, 3, false, Image.FORMAT_RGBA8)
		img.fill(Color(0.83, 0.63, 0.09, 1.0))
		sprite.texture = ImageTexture.create_from_image(img)
	sprite.centered = true
	add_child(sprite)

func _physics_process(delta: float) -> void:
	lifetime -= delta
	if lifetime <= 0.0:
		queue_free()
		return
	
	if not is_instance_valid(target) or not target.alive:
		queue_free()
		return
	
	var dir: Vector2 = (target.global_position - global_position)
	var dist: float = dir.length()
	
	if dist < 12.0:
		target.take_damage(damage)
		queue_free()
		return
	
	velocity = dir.normalized() * speed
	rotation = dir.angle()
	move_and_slide()
