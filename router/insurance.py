from fastapi import APIRouter
from fastapi.responses import JSONResponse
from schemas import UserInput
from schemas import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION


# schemas.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/insurance_premium",
    tags=["insurance_premium"],
)


# human readable
@router.get('/')
def home():
    return {'message': 'Insurance Premium Prediction API'}


# machine readable
@router.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }


@router.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:

        prediction = predict_output(user_input)

        return JSONResponse(status_code=200, content={'response': prediction})

    except Exception as e:

        return JSONResponse(status_code=500, content=str(e))
