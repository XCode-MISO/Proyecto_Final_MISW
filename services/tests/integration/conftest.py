
import os
import pathlib
import socket
import subprocess
import time

import pytest

# ───────────────────────────────────────────────────────────────
# Configuración
# ───────────────────────────────────────────────────────────────
HERE = pathlib.Path(__file__).parent
COMPOSE_FILE = HERE / "docker-compose.yml"
COMPOSE_CMD = ["docker", "compose", "-f", str(COMPOSE_FILE)]

# Puertos donde expusiste cada micro en el compose
PORTS = {
    "compras": 5001,
    "pedidos": 5002,
    "inventarios": 5003,
}

WAIT_SECONDS = 40          # tiempo máximo para que arranquen los servicios
CHECK_INTERVAL = 1         # intervalo entre intentos

# ───────────────────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────────────────
def _is_port_open(host: str, port: int) -> bool:
    """True si algo está escuchando en host:port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex((host, port)) == 0


def _wait_for_ports(ports: dict[str, int], timeout: int = WAIT_SECONDS):
    """Bloquea hasta que todos los puertos estén abiertos o hasta timeout."""
    deadline = time.time() + timeout
    pending = ports.copy()

    while pending and time.time() < deadline:
        for name, port in list(pending.items()):
            if _is_port_open("localhost", port):
                pending.pop(name)
        time.sleep(CHECK_INTERVAL)

    if pending:
        raise RuntimeError(
            f"Los siguientes servicios no arrancaron a tiempo: {list(pending.keys())}"
        )


# ───────────────────────────────────────────────────────────────
# Fixtures
# ───────────────────────────────────────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def docker_compose_up_down():
    """
    Levanta el stack definido en docker‑compose.yml al iniciar la sesión
    y lo baja al finalizar.
    """
    print("🔹  Levantando entorno de integración con Docker Compose …")
    subprocess.run(
        COMPOSE_CMD + ["up", "--build", "-d"],
        check=True,
        cwd=HERE,
    )

    try:
        _wait_for_ports(PORTS)
        print("✅  Todos los servicios responden, ¡a probar!")
        yield
    finally:
        print("🔻  Cerrando entorno de integración …")
        subprocess.run(
            COMPOSE_CMD + ["down", "-v"],
            check=True,
            cwd=HERE,
        )


@pytest.fixture(scope="session")
def urls() -> dict[str, str]:
    """Devuelve los endpoints base de cada micro."""
    return {
        name: f"http://localhost:{port}"
        for name, port in PORTS.items()
    }