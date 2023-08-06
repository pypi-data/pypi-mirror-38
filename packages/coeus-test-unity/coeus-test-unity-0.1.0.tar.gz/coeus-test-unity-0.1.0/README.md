# Coeus-Unity

## About
Coeus-Unity is a collection of commands and assertions built on `coeus-test` package for python. These commands support remote integration tests in Unity with the use of the C# Coeus test framework.

## Setup
Simply install the requirement into your package.

```python
pip install coeus-test-unity
```

## Commands
Commands offer no response validation. You can use assertions for that.

```python
import commands

response = commands.query_transform_exists(cli, "My/Transform Hierarchy/Object (Clone)")
response = commands.query_scene_loaded(cli, "AppSetup")
response = commands.query_renderer_visible(cli, "My/Target/Object (Clone)")

response = commands.await_transform_exists(cli, "My/Transform Hierarchy/Object (Clone)")
# Waits for renderer to become not visible based on False...
response = commands.await_renderer_visible(cli, "My/Transform Hierarchy/Object (Clone)", False)
response = commands.await_scene_loaded(cli, "AppSetup")
```