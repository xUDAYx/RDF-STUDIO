{
    "rules": [
        {
            "description": "No alert function should be used",
            "pattern": "\\balert\\b\\s*\\("
        },
        {
            "description": "No console.log should be used",
            "pattern": "\\bconsole\\.log\\b\\s*\\("
        },
        {
            "description": "No eval function should be used",
            "pattern": "\\beval\\b\\s*\\("
        },
        {
            "description": "No innerHTML property should be used",
            "pattern": "\\binnerHTML\\b"
        },
        {
            "description": "No document.write should be used",
            "pattern": "\\bdocument\\.write\\b\\s*\\("
        }
    ]
}
