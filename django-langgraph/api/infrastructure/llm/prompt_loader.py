from pathlib import Path
import yaml

def load_prompt(
    service: str,
    prompt_file: str,
    prompt_name: str
) -> dict:
    prompt_path = (
        Path(__file__).resolve().parents[2]
        / "services"
        / service
        / "prompts"
        / f"{prompt_file}.yaml"
    )

    with prompt_path.open(encoding="utf-8") as file:
        prompts = yaml.safe_load(file)

    try:
        return prompts[prompt_name]
    except KeyError as exc:
        raise ValueError(
            f"Prompt '{prompt_name}' not found in '{prompt_file}'"
        ) from exc