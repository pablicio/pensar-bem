<?php

declare(strict_types=1);

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

class LivroFactory extends Factory
{
    public function definition(): array
    {
        return [
            'titulo' => fake()->sentence(3),
            'autor' => fake()->name(),
            'isbn' => fake()->unique()->isbn13(),
            'assunto' => fake()->randomElement([
                'literatura', 'didatico', 'infantil',
            ]),
            'ano' => fake()->numberBetween(1890, 2026),
        ];
    }

    public function infantil(): static
    {
        return $this->state(fn (): array => [
            'assunto' => 'infantil',
            'ano' => fake()->numberBetween(2000, 2026),
        ]);
    }
}
