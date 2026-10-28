final class ConferidorDeSenha
{
    public function confere(Usuario $u, string $senha): bool
    {
        if ($this->ehMd5Legado($u->senha)) {
            if (!hash_equals($u->senha, md5($senha))) {
                return false;
            }

            $u->forceFill(['senha' => Hash::make($senha)])->save();

            return true;
        }

        if (!Hash::check($senha, $u->senha)) {
            return false;
        }

        if (Hash::needsRehash($u->senha)) {
            $u->forceFill(['senha' => Hash::make($senha)])->save();
        }

        return true;
    }

    private function ehMd5Legado(string $hash): bool
    {
        return (bool) preg_match('/^[a-f0-9]{32}$/', $hash);
    }
}
