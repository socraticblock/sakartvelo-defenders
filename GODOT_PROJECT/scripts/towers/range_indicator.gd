## RangeIndicator — Draws tower range circle
extends Node2D

var range_radius: float = 150.0

func _draw() -> void:
	draw_arc(Vector2.ZERO, range_radius, 0, TAU, 64, Color(1, 1, 1, 0.3), 2.0, true)
