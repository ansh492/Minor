

# File Store Module

## Files
- **fileStore.ts** (or .js) - Central source of truth for file management, sidebar UI, and file operations

## Variables
- **fileStore**: Object that maps filenames to their content strings; serves as the central data store for all open files
- **activeFile**: String containing the name of the currently open/editing file
- **mainFile**: String containing the name of the main/primary file (marked with ★)

## Functions Available

### File Operations
- **setActiveFile(name)**: Updates the activeFile variable to the specified filename
- **setMainFile(name)**: Updates the mainFile variable and triggers sidebar re-render
- **putFile(name, content)**: Adds a new file or overwrites existing file content; triggers sidebar re-render
- **renameFile(oldName, newName)**: Renames a file while preserving content; updates activeFile/mainFile references if they were renamed
- **deleteFile(name)**: Deletes a file, but prevents deletion of the last file; updates activeFile/mainFile to another available file

### UI Rendering
- **renderFileInfo()**: Updates the file information bar displaying:
  - Current editing file with "main" badge if applicable
  - Main file name
  - Total count of open files
- **renderSidebar()**: Rebuilds the entire sidebar UI including:
  - Header with "New" button
  - File list with active/main indicators
  - Action buttons (set as main, rename, delete) for each file

### Navigation
- **switchToFile(name)**: Switches the editor to a different file by:
  1. Saving current textarea content to the active file
  2. Updating activeFile reference
  3. Re-rendering UI components
  4. Triggering external callbacks if defined

## Flow

### Initial State
```
Start
  ↓
Initialize fileStore with default "main.typ"
  ↓
Set activeFile = "main.typ"
  ↓
Set mainFile = "main.typ"
```

### New File Creation Flow
```
User clicks "+ New" button
  ↓
Prompt for filename
  ↓
Validate/add .typ extension if missing
  ↓
call putFile(name, "")
  ↓
fileStore[name] = ""
  ↓
renderSidebar() → rebuilds UI
  ↓
switchToFile(newFile)
  ├─ Save current textarea content to old activeFile
  ├─ Update activeFile = newFile
  ├─ renderSidebar() → updates UI highlighting
  ├─ renderFileInfo() → updates file info bar
  └─ Trigger onActiveFileChange callback
```

### File Rename Flow
```
User clicks "✎" on a file
  ↓
Prompt for new filename
  ↓
Validate new name (not empty, not existing)
  ↓
call renameFile(oldName, newName)
  ├─ Copy content: fileStore[newName] = fileStore[oldName]
  ├─ Delete old: delete fileStore[oldName]
  ├─ If activeFile was renamed: activeFile = newName
  ├─ If mainFile was renamed: mainFile = newName
  └─ renderSidebar() → rebuilds UI
  ↓
Trigger onActiveFileChange callback
```

### File Deletion Flow
```
User clicks "✕" on a file
  ↓
Confirm deletion with user
  ↓
Check if this is the last file (keys.length ≤ 1)
  ↓ If true → Cancel (prevent deletion)
  ↓ If false → call deleteFile(name)
  ├─ delete fileStore[name]
  ├─ If deleted file was activeFile: activeFile = first remaining file
  ├─ If deleted file was mainFile: mainFile = first remaining file
  └─ renderSidebar() → rebuilds UI
  ↓
Trigger onActiveFileChange callback
```

### File Switching Flow
```
User clicks a file name in sidebar
  ↓
call switchToFile(selectedFile)
  ├─ Get textarea element
  ├─ Save current content: fileStore[activeFile] = textarea.value
  ├─ Update activeFile = selectedFile
  ├─ renderSidebar() → updates active highlighting
  ├─ renderFileInfo() → updates editing/main indicators
  └─ Trigger onActiveFileChange callback
```

### Set as Main File Flow
```
User clicks "★" on a file
  ↓
call setMainFile(selectedFile)
  ├─ Update mainFile = selectedFile
  ├─ renderSidebar() → rebuilds UI (updates ★ indicators)
  └─ Trigger onMainFileChange callback
```

### Sidebar Rendering Flow
```
renderSidebar() called
  ↓
Get sidebar DOM element
  ↓
Clear existing content
  ↓
Create header with title and "+ New" button
  ↓
For each file in fileStore:
  ├─ Create list item
  ├─ Set classes (active/main styling)
  ├─ Add filename (click to switch)
  ├─ Add action buttons:
  │   ├─ ★ (set as main) if not main file
  │   ├─ ✎ (rename)
  │   └─ ✕ (delete)
  └─ Add to list
  ↓
Append list to sidebar
  ↓
Call renderFileInfo()
```

### File Info Bar Update Flow
```
renderFileInfo() called
  ↓
Get file-info DOM element
  ↓
Check if activeFile === mainFile
  ↓
Generate HTML with:
  ├─ Editing: [activeFile] + badge if main
  ├─ Main: [mainFile]
  └─ Total files count
  ↓
Update DOM element innerHTML
```

### External Callbacks
```
When active file changes (via switchToFile or deleteFile):
  └─ if window.onActiveFileChange exists → call with new activeFile

When main file changes (via setMainFile):
  └─ if window.onMainFileChange exists → call with new mainFile
```
