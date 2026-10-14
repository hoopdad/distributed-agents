def agent_metadata(name, body):
    latest = body["versions"]["latest"]
    if not isinstance(latest["version"], str) or not latest["version"]:
        raise ValueError("Agent metadata has no version")
    return {
        "agent": name, "exists": True, "version": latest["version"],
        "latest_field_names": sorted(latest), "status": latest.get("status"),
        "instance_identity": latest.get("instance_identity"),
        "endpoint": latest.get("endpoint"),
        "code_configuration": latest.get("definition", {}).get("code_configuration"),
        "error": {key: latest["error"][key] for key in ("code", "message")
                  if key in latest["error"]} if isinstance(latest.get("error"), dict) else latest.get("error"),
    }
