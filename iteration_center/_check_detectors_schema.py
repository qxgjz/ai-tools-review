# -*- coding: utf-8 -*-
"""确认所有 hallucination 检测器 + PIIDetector 的 evaluate 参数要求"""
import inspect
from llmevalkit.hallucination import (
    CausalHallucination, ConfidenceCalibration, ContradictionDetector,
    EntityHallucination, FabricatedInfo, InstructionHallucination,
    NegationHallucination, NumericHallucination,
)
from llmevalkit.compliance import PIIDetector

for name, cls in [
    ('CausalHallucination', CausalHallucination), ('ConfidenceCalibration', ConfidenceCalibration),
    ('ContradictionDetector', ContradictionDetector), ('EntityHallucination', EntityHallucination),
    ('FabricatedInfo', FabricatedInfo), ('InstructionHallucination', InstructionHallucination),
    ('NegationHallucination', NegationHallucination), ('NumericHallucination', NumericHallucination),
    ('PIIDetector', PIIDetector),
]:
    print(f'=== {name} ===')
    try:
        sig = inspect.signature(cls.__init__)
        print('  __init__:', list(sig.parameters.keys()))
    except Exception as e:
        print('  __init__ 失败:', e)
    try:
        d = cls(use_llm=False) if name != 'PIIDetector' else cls()
        sig = inspect.signature(d.evaluate)
        print('  evaluate 签名:', sig)
        try:
            print('  required_fields:', d.required_fields)
        except Exception:
            pass
    except Exception as e:
        print('  evaluate 失败:', str(e)[:150])
    print()
