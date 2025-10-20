import subprocess
import sys


def run():
    try:
        print("Running pytest...")
        res = subprocess.run([sys.executable, "-m", "pytest", "-q"], check=False)
        return res.returncode
    except Exception:
        print("pytest not available; running a simple smoke test")
        # simple smoke test: import main and create agent with dummy envs
        import os
        os.environ["OPENAI_API_KEY"] = "sk-test"
        os.environ["TAVILY_API_KEY"] = "tv-test"
        sys.path.insert(0, "src")
        try:
            from main import create_agent
            print("Creating agent...")
            agent = create_agent()
            print("Agent created:", agent.get_agent_info()["name"])
            return 0
        except Exception as e:
            print("Smoke test failed:", e)
            return 1


if __name__ == "__main__":
    raise SystemExit(run())
