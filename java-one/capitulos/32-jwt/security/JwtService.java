@Service
public class JwtService {

    private final SecretKey key;
    private final long expiracaoSegundos;

    public JwtService(
            @Value("${app.jwt.secret}") String secret,
            @Value("${app.jwt.expiration}") long expiracao) {
        this.key = Keys.hmacShaKeyFor(secret.getBytes());
        this.expiracaoSegundos = expiracao;
    }

    public String gerar(String email, Role role) {
        Instant agora = Instant.now();
        return Jwts.builder()
                .subject(email)
                .claim("role", role.name())
                .issuedAt(Date.from(agora))
                .expiration(Date.from(
                        agora.plusSeconds(expiracaoSegundos)))
                .signWith(key)
                .compact();
    }

    public String emailDo(String token) {
        return Jwts.parser()
                .verifyWith(key)
                .build()
                .parseSignedClaims(token)
                .getPayload()
                .getSubject();
    }
}
