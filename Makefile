SCRIPTS := $(wildcard scripts/*.py)
TOPICS  := $(patsubst scripts/%.py,%,$(SCRIPTS))
TARGETS := $(addprefix topic/,$(TOPICS))

.PHONY: all $(TARGETS) clean watch install

all: $(TARGETS)

$(TARGETS): topic/%: scripts/%.py outputs
	python -m scripts.$*

outputs:
	mkdir -p outputs

clean:
	rm -f outputs/*.png outputs/*.gif

watch:
	@which fswatch > /dev/null || (echo "install fswatch: brew install fswatch"; exit 1)
	@while true; do \
		fswatch -1 scripts/ physics/ theme.py animate.py builder.py 2>/dev/null; \
		$(MAKE) all; \
	done

install:
	pip install -e .
