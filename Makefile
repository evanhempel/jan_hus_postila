# Makefile for generating English outputs from Czech sermons

# Default models for translation
MODELS := openrouter/openai/gpt-5.1 openrouter/amazon/nova-2-lite-v1:free openrouter/google/gemini-3-pro

# Default summary model
SUMMARY_MODEL := openrouter/deepseek/deepseek-chat

# Default target
all: summary translations

# Generate summary for a specific file
summary:
	@if [ -z "$(SERMON)" ]; then \
		echo "Usage: make summary SERMON=path/to/sermon.cs.md"; \
		exit 1; \
	fi
	@echo "Generating summary for $(SERMON)..."
	time cat $(SERMON) | llm -m $(SUMMARY_MODEL) -s "$(cat summary.prompt)" > $(basename $(SERMON)).aa.summary.en.md

# Generate translations for a specific file
translations:
	@if [ -z "$(SERMON)" ]; then \
		echo "Usage: make translations SERMON=path/to/sermon.cs.md"; \
		exit 1; \
	fi
	@echo "Generating translations for $(SERMON)..."
	$(foreach model,$(MODELS),\
		time cat $(SERMON) | llm -m $(model) -s "$(cat translation.prompt)" > $(basename $(SERMON)).en_$(subst /,_,$(subst :,_,$(model))).md; \
	)

# Generate all outputs for a specific file
%:
	@if [ -f "$(SERMON)" ]; then \
		if [ "$(MAKECMDGOALS)" = "summary" ]; then \
			$(MAKE) summary SERMON=$(SERMON); \
		elif [ "$(MAKECMDGOALS)" = "translations" ]; then \
			$(MAKE) translations SERMON=$(SERMON); \
		else \
			echo "Usage: make [summary|translations] SERMON=path/to/sermon.cs.md"; \
			exit 1; \
		fi; \
	else \
		echo "Error: File $(SERMON) not found"; \
		exit 1; \
	fi

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@rm -f sermons/*.aa.summary.en.md
	@rm -f sermons/*.en_*.md

# Show help
help:
	@echo "Available targets:"
	@echo "  all         - Generate all outputs (summary and translations)"
	@echo "  summary     - Generate summary only (requires SERMON variable)"
	@echo "  translations - Generate translations only (requires SERMON variable)"
	@echo "  clean       - Remove all generated files"
	@echo "  help        - Show this help message"
	@echo ""
	@echo "Usage examples:"
	@echo "  make summary SERMON=sermons/03_first_sunday_of_advent_readings.cs.md"
	@echo "  make translations SERMON=sermons/03_first_sunday_of_advent_readings.cs.md"
	@echo "  make all SERMON=sermons/03_first_sunday_of_advent_readings.cs.md"
