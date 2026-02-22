"""
AGSM Rules Engine
Detect specific Australian Government Style Manual violations
"""

import re
from typing import List, Dict, Tuple


class AGSMRules:
    """Detect and suggest fixes for AGSM style guide violations"""
    
    # Common formal → plain language replacements
    WORD_REPLACEMENTS = {
        # Verbs
        r'\bfacilitate\b': 'help',
        r'\butilize\b': 'use',
        r'\bcommence\b': 'start',
        r'\bimplement\b': 'carry out',
        r'\bdemonstrate\b': 'show',
        r'\bidentify\b': 'find',
        r'\bprovide\b': 'give',
        r'\bobtain\b': 'get',
        r'\bpurchase\b': 'buy',
        r'\bterminate\b': 'end',
        r'\bretain\b': 'keep',
        r'\bnotify\b': 'tell',
        r'\badvise\b': 'tell',
        
        # Phrases
        r'\bprior to\b': 'before',
        r'\bsubsequent to\b': 'after',
        r'\bin order to\b': 'to',
        r'\bfor the purpose of\b': 'to',
        r'\bwith regard to\b': 'about',
        r'\bin relation to\b': 'about',
        r'\bin accordance with\b': 'following',
        r'\bas a consequence of\b': 'because',
        r'\bdue to the fact that\b': 'because',
        r'\bin the event that\b': 'if',
        r'\bat this point in time\b': 'now',
        r'\bat the present time\b': 'now',
        r'\bin the near future\b': 'soon',
        r'\ba number of\b': 'several',
        r'\ba majority of\b': 'most',
        
        # Nouns
        r'\brequirement\b': 'what you need',
        r'\bapplicant\b': 'you',
        r'\bindividual\b': 'person',
        r'\bcommencement\b': 'start',
        r'\bconclusion\b': 'end',
        r'\butilization\b': 'use',
        r'\bimplementation\b': 'carrying out',
        
        # Adjectives/Adverbs
        r'\badditional\b': 'more',
        r'\bsufficient\b': 'enough',
        r'\bnumerous\b': 'many',
        r'\bapproximate\b': 'about',
    }
    
    # Passive voice indicators (common patterns)
    PASSIVE_INDICATORS = [
        r'\bis required\b',
        r'\bare required\b',
        r'\bmust be\b',
        r'\bshould be\b',
        r'\bcan be\b',
        r'\bwill be\b',
        r'\bhas been\b',
        r'\bhave been\b',
        r'\bwas\b.*\b(submitted|provided|completed|approved|rejected)',
        r'\bwere\b.*\b(submitted|provided|completed|approved|rejected)',
        r'\bto be\b.*\b(submitted|provided|completed|approved|rejected)',
    ]
    
    # Nominalizations (turning verbs into nouns - bad for readability)
    NOMINALIZATIONS = {
        r'\bapplication\b.*\bof\b': 'apply',
        r'\bimplementation\b.*\bof\b': 'implement',
        r'\bcompletion\b.*\bof\b': 'complete',
        r'\bassessment\b.*\bof\b': 'assess',
        r'\bconsideration\b.*\bof\b': 'consider',
        r'\bestablishment\b.*\bof\b': 'establish',
        r'\bdevelopment\b.*\bof\b': 'develop',
    }
    
    def __init__(self):
        # Compile patterns for efficiency
        self.word_patterns = {
            re.compile(pattern, re.IGNORECASE): replacement
            for pattern, replacement in self.WORD_REPLACEMENTS.items()
        }
        
        self.passive_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.PASSIVE_INDICATORS
        ]
        
        self.nominalization_patterns = {
            re.compile(pattern, re.IGNORECASE): replacement
            for pattern, replacement in self.NOMINALIZATIONS.items()
        }
    
    def find_violations(self, text: str) -> Dict[str, List[Dict]]:
        """
        Find all AGSM violations in text
        Returns categorized violations with line numbers and suggestions
        """
        violations = {
            'formal_words': [],
            'passive_voice': [],
            'nominalizations': [],
        }
        
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check formal words
            for pattern, replacement in self.word_patterns.items():
                for match in pattern.finditer(line):
                    violations['formal_words'].append({
                        'line': line_num,
                        'original': match.group(0),
                        'suggestion': replacement,
                        'context': line.strip(),
                        'position': match.start()
                    })
            
            # Check passive voice patterns
            for pattern in self.passive_patterns:
                for match in pattern.finditer(line):
                    violations['passive_voice'].append({
                        'line': line_num,
                        'phrase': match.group(0),
                        'context': line.strip(),
                        'position': match.start()
                    })
            
            # Check nominalizations
            for pattern, verb_form in self.nominalization_patterns.items():
                for match in pattern.finditer(line):
                    violations['nominalizations'].append({
                        'line': line_num,
                        'phrase': match.group(0),
                        'suggestion': f'Use verb form: {verb_form}',
                        'context': line.strip(),
                        'position': match.start()
                    })
        
        return violations
    
    def generate_fix_instructions(self, violations: Dict[str, List[Dict]]) -> str:
        """
        Generate human-readable instructions for LLM to fix violations
        """
        instructions = []
        
        # Formal words
        if violations['formal_words']:
            instructions.append("REPLACE FORMAL WORDS:")
            seen = set()
            for v in violations['formal_words']:
                key = (v['original'].lower(), v['suggestion'])
                if key not in seen:
                    instructions.append(f"  • '{v['original']}' → '{v['suggestion']}'")
                    seen.add(key)
        
        # Passive voice
        if violations['passive_voice']:
            instructions.append("\nCONVERT PASSIVE TO ACTIVE VOICE:")
            for v in violations['passive_voice'][:3]:  # Show first 3 examples
                instructions.append(f"  • Line {v['line']}: {v['context']}")
        
        # Nominalizations
        if violations['nominalizations']:
            instructions.append("\nREPLACE NOMINALIZATIONS WITH VERBS:")
            for v in violations['nominalizations']:
                instructions.append(f"  • {v['suggestion']}")
        
        if not any(violations.values()):
            return "No specific AGSM violations found. Focus on simplifying vocabulary."
        
        return '\n'.join(instructions)
    
    def get_violation_count(self, violations: Dict[str, List[Dict]]) -> int:
        """Total number of violations found"""
        return sum(len(v) for v in violations.values())
    
    def quick_check(self, text: str) -> Tuple[int, str]:
        """
        Quick check for violations
        Returns: (violation_count, summary_message)
        """
        violations = self.find_violations(text)
        count = self.get_violation_count(violations)
        
        if count == 0:
            return 0, "No AGSM violations detected"
        
        summary = []
        if violations['formal_words']:
            summary.append(f"{len(violations['formal_words'])} formal words")
        if violations['passive_voice']:
            summary.append(f"{len(violations['passive_voice'])} passive voice patterns")
        if violations['nominalizations']:
            summary.append(f"{len(violations['nominalizations'])} nominalizations")
        
        return count, f"Found: {', '.join(summary)}"


# Example usage
if __name__ == "__main__":
    checker = AGSMRules()
    
    test_text = """
    The Department of Infrastructure is responsible for the administration of programs.
    Applications must be submitted prior to the closing date.
    Failure to comply may result in the application being deemed ineligible.
    """
    
    violations = checker.find_violations(test_text)
    print("Violations found:")
    print(checker.generate_fix_instructions(violations))
    print()
    count, summary = checker.quick_check(test_text)
    print(f"Total: {count} violations")
    print(summary)
