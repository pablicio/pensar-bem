package com.loja.catalog.auth;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final AuthenticationManager manager;
    private final JwtService jwt;
    private final UserRepository users;

    @PostMapping("/login")
    public LoginResponse login(@Valid @RequestBody LoginRequest req) {
        manager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        req.email(), req.password()));

        User user = users.findByEmail(req.email()).orElseThrow();
        return new LoginResponse(
                jwt.gerar(user.getEmail(), user.getRole()), 3600);
    }
}
