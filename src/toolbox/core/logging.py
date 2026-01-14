import logging
import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path
from rich.logging import RichHandler

class LedgerFormatter(logging.Formatter):
    """Immutable Ledger Formatter that hashes each entry with the previous one."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev_hash = "0" * 64
        self.ledger_path = Path("toolbox.ledger")
        if self.ledger_path.exists():
            try:
                last_line = self.ledger_path.read_text().splitlines()[-1]
                last_entry = json.loads(last_line)
                self.prev_hash = last_entry.get("hash", "0" * 64)
            except Exception:
                pass

    def format(self, record):
        msg = record.getMessage()
        timestamp = datetime.utcnow().isoformat()
        
        # Create hash of the current entry + previous hash
        data_to_hash = f"{timestamp}|{record.levelname}|{msg}|{self.prev_hash}"
        current_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
        
        log_record = {
            "timestamp": timestamp,
            "level": record.levelname,
            "message": msg,
            "prev_hash": self.prev_hash,
            "hash": current_hash
        }
        
        self.prev_hash = current_hash
        
        # Write to ledger file (append only)
        with open(self.ledger_path, "a") as f:
            f.write(json.dumps(log_record) + "\n")
            
        return f"[{timestamp}] {record.levelname}: {msg} (Hash: {current_hash[:8]})"

class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for machine-readable logs."""
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "func": record.funcName
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def setup_logging(level=logging.INFO, log_file: Path = None, json_format: bool = False):
    """
    Setup structured logging using Rich for console and standard logging for files.
    """
    # Create logger
    logger = logging.getLogger("toolbox")
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []

    if json_format:
        # JSON Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(JsonFormatter())
    else:
        # Rich Console handler
        console_handler = RichHandler(
            rich_tracebacks=True,
            markup=True,
            show_time=False,
            show_path=False
        )
    
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    # File handler (if provided)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        # Use Immutable Ledger for file logs by default in Phase 7
        file_handler.setFormatter(LedgerFormatter())
        logger.addHandler(file_handler)

    return logger

# Global logger instance
logger = logging.getLogger("toolbox")
