File.write("lista.lock", Process.pid.to_s)

begin
  gerar_lista
ensure
  File.delete("lista.lock")
end
