# Makefile for generating English outputs from Czech sermons

# Default target
all: summary translations

# Generate summary
summary:
	@echo "Generating summary..."
	@time cat sermons/03_first_sunday_of_advent_readings.cs.md | llm -m openrouter/deepseek/deepseek-chat -s "$(cat summary.prompt)" > sermons/03_first_sunday_of_advent_readings.aa.summary.en.md

# Generate translations
translations:
	@echo "Generating translations..."
	@time cat sermons/04_second_sunday_of_advent_readings.cs.md | llm -m openrouter/openai/gpt-5.1 -s "$(cat translation.prompt)" > sermons/04_second_sunday_of_advent_readings.en_gpt5.1.md
	@time cat sermons/04_second_sunday_of_advent_readings.cs.md | llm -m openrouter/amazon/nova-2-lite-v1:free -s "$(cat translation.prompt)" > sermons/04_second_sunday_of_advent_readings.en_nova2.md
	@time cat sermons/04_second_sunday_of_advent_readings.cs.md | llm -m openrouter/google/gemini-3-pro -s "$(cat translation.prompt)" > sermons/04_second_sunday_of_advent_readings.en_gemini3.md

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@rm -f sermons/*.aa.summary.en.md
	@rm -f sermons/*.en_*.md

# Show help
help:
	@echo "Available targets:"
	@echo "  all         - Generate all outputs (summary and translations)"
	@echo "  summary     - Generate summary only"
	@echo "  translations - Generate translations only"
	@echo "  clean       - Remove all generated files"
	@echo "  help        - Show this help message"
