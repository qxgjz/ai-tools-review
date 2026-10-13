# -*- coding: utf-8 -*-
import inspect
from zens_ink import content_qc
print(inspect.signature(content_qc.check_draft))
print('---')
print(inspect.getdoc(content_qc.check_draft)[:800] if inspect.getdoc(content_qc.check_draft) else 'no doc')
