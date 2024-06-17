from fastapi import Request, APIRouter, HTTPException, status
from .schema import Applicant

router = APIRouter(prefix='/applicant', tags=['applicant'])

@router.get("/")
async def root_():
    try:
        return "hello root"
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    
@router.post("/add")
async def add_(request: Request, apl: Applicant):
    try:
        odoo = request.app.state.odoo
        applicant = odoo.env['hr.applicant']
        a_id = applicant.create({
            'stage_id': 1,
            'company_id': 1,
            'job_id': 3,
            'name': 'Sales Agent',
            'partner_name': apl.name,
            # 'partner_phone': apl.phone,
            'email_from': apl.email,
            'kanban_state': 'normal',
        })

        skill = odoo.env['hr.applicant.skill']
        skill.create({
            'applicant_id': a_id,
            'skill_id': 1, # 2 french, 1 english
            'skill_level_id': int(apl.eLevel), # level
            'skill_type_id': 1, 
        })
        # skill.create({
        #     'applicant_id': a_id,
        #     'skill_id': 2, # 2 french, 1 english
        #     'skill_level_id': 2, # level
        #     'skill_type_id': 1, 
        # })
        return {
            'applicant_id': a_id
        }
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
