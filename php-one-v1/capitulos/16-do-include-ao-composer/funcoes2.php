<?php

function formatarData(string $iso): string
{
    return date('d/m/Y', strtotime($iso));
}
