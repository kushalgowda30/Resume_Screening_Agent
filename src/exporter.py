from openpyxl import Workbook


def export_to_excel(results, filename="output/screening_results.xlsx"):

    wb = Workbook()
    ws = wb.active

    ws.title = "Resume Screening"

    ws.append(["Rank", "Resume", "Score", "Recommendation"])

    for rank, (name, score, recommendation) in enumerate(results, start=1):

        ws.append([
            rank,
            name,
            f"{score:.2f}",
            recommendation
        ])

    wb.save(filename)

    print(f"\nResults exported to {filename}")