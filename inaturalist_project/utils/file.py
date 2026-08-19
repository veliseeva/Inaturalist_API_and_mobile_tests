def abs_path_from_project(relative_path: str):
    import inaturalist_project
    from pathlib import Path

    return (
        Path(inaturalist_project.__file__)
        .parent.parent.joinpath(relative_path)
        .absolute()
        .__str__()
    )