<?php

if (!function_exists('formatarData')) {
    function formatarData(string $iso): string
    {
        return date('d/m/y', strtotime($iso));
    }
}
