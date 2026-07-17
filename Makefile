PHASE1_SCRIPTS := $(wildcard scripts/phase_1/*.py)
PHASE2_SCRIPTS := $(wildcard scripts/phase_2/*.py)
PHASE1_TOPICS  := $(patsubst scripts/phase_1/%.py,phase_1/%,$(PHASE1_SCRIPTS))
PHASE2_TOPICS  := $(patsubst scripts/phase_2/%.py,phase_2/%,$(PHASE2_SCRIPTS))
TOPICS         := $(PHASE1_TOPICS) $(PHASE2_TOPICS)
TARGETS        := $(addprefix topic/,$(TOPICS))

.PHONY: all $(TARGETS) clean watch install

all: $(TARGETS)

topic/phase_1/%: scripts/phase_1/%.py outputs
	python -m scripts.phase_1.$*

topic/phase_2/%: scripts/phase_2/%.py outputs
	python -m scripts.phase_2.$*

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
