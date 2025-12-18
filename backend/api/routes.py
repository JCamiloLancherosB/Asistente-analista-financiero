"""API routes for the financial assistant."""

import io

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.models.schemas import (
    ChatRequest,
    ChatResponse,
    FinancialData,
    UploadResponse,
)
from backend.services.vertex_ai import get_vertex_service
from backend.tools.financial_tools import financial_tools

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint that processes messages using Gemini model.

    Args:
        request: Chat request with messages and optional parameters

    Returns:
        Chat response with assistant message and tool calls
    """
    try:
        # Generate response using Vertex AI
        vertex_service = get_vertex_service()
        result = await vertex_service.generate_response(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        # Process any tool calls
        if result.get("tool_calls"):
            for tool_call in result["tool_calls"]:
                tool_name = tool_call["name"]
                tool_args = tool_call["arguments"]

                # Execute the tool function
                if hasattr(financial_tools, tool_name):
                    tool_func = getattr(financial_tools, tool_name)
                    try:
                        # Execute tool but don't need to use result here
                        # The model will handle the tool results in its response
                        tool_func(**tool_args)
                    except Exception as tool_err:
                        print(f"Error executing tool {tool_name}: {tool_err}")

        return ChatResponse(
            response=result["response"],
            tool_calls=result.get("tool_calls"),
            model_used=result["model_used"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}") from e


@router.post("/upload", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)) -> UploadResponse:
    """
    Upload and parse CSV file with financial data.

    Args:
        file: CSV file to upload

    Returns:
        Summary of uploaded data
    """
    # Validate file type first (before try block)
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    try:
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        # Convert to list of dictionaries
        data = df.to_dict("records")

        # Store in financial tools
        financial_tools.store_financial_data(data, dataset_name="uploaded")

        # Create summary
        data_summary = FinancialData(
            data=data[:10],  # Return first 10 rows as sample
            columns=list(df.columns),
            row_count=len(df),
        )

        return UploadResponse(
            message=f"Successfully uploaded {len(df)} rows of financial data",
            data_summary=data_summary,
        )

    except pd.errors.EmptyDataError as e:
        raise HTTPException(status_code=400, detail="CSV file is empty") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}") from e


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "financial-assistant"}
