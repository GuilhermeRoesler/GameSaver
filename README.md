# GameSaver

A powerful tool to backup and restore game save files across different computers.

## Features

- Automatically detects installed games from a predefined database
- Backs up save files to a specified destination
- User-friendly configuration through JSON files
- Support for custom game paths
- Cross-platform compatibility

## Installation

1. Download the latest release from the releases page
2. Extract the files to your desired location
3. Run the executable

## Configuration

### Settings (settings.json)

The application uses a settings file that contains:

- `user_location`: Path to your user directory (default is home directory)
- `destination_location`: Where save backups will be stored
- `mode`: Operation mode (`collect` or `spread`)

### Games Database (games.json)

Add your games in the following format:

```json
{
    "game": "Game Name",
    "path": "\\AppData\\Roaming\\YourGame",
    "last_save": ""
}
```

## Usage

1. Launch the application
2. Verify/modify the default settings when prompted
3. Choose operation mode:
   - `collect`: Backup save files
   - `spread`: Restore save files (coming soon)
4. Confirm the operation

## Supported Games

The tool comes with a pre-configured database of common games. You can add more games by editing the `games.json` file.

## Directory Structure

```
GameSaver/
├── settings.json
├── games.json
├── games_database.json
└── SAVES/
    └── [Game Save Folders]
```

## Requirements

- Windows/Linux/MacOS
- Python 3.6+ (if running from source)
- Write permissions in destination directory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all contributors who have helped with the games database
- Special thanks to the gaming community for feedback and support

## Support

For issues and feature requests, please use the GitHub issue tracker.
